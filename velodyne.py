#!/usr/bin/python

"""
    read or unpack Velodyne VLP-16 data
    usage:
        ./velodyne.py <read | unpack> [bin file dir]
"""

import os
import csv
import sys
import socket
import glob
from datetime import datetime, timedelta
import struct
import time
import traceback
import numpy as np
from multiprocessing import Process, Queue, Pool


import VLP16defs
from ROS_ts import ROS_ts


#%%
def read_ts(file):
    ts = []
    with open(file, 'rt') as ts_f:
        for line in ts_f:
            t = line.split()[0].split('.')
            ts_s = int(t[0])
            ts_ns = int(t[1])
            ts.append( ROS_ts(ts_s, ts_ns))
    return np.array(ts)


#%%

point_keys = ['az', 'dist', 'intensity', 'omega', 'ts']    
    
def read_velo_file(path):
    
    packet_cnt = 0;
    ts_file = os.path.join(path,'timestampsU.txt')
    time_stamps = read_ts(ts_file)
    
    v_file = os.path.join(path, 'velodyne.bin')
    points = []
    
    base_ts = ROS_ts(0)
    with open(v_file, 'rb') as vf:
        d_az = 0.41111;  #default az step    
        old_az = -1;

        while (1):
            #scan = np.fromfile(vf, dtype=np.uint8, count=PACKET_SIZE);
            scan = vf.read(PACKET_SIZE);
            if (len(scan) < PACKET_SIZE ):
                break;

            ts=struct.unpack_from('<I', scan, TS_OFFSET)[0]
                
            if (base_ts == 0):
                base_ts = time_stamps[0] - ts * 1000;

            firing_ts = base_ts + ts * 1000;
            #print (firing_ts, time_stamps[packet_cnt], firing_ts-time_stamps[packet_cnt])

            for block in range(BLOCKS_PER_PACKET):
                offset = block * SIZE_BLOCK;
                head=struct.unpack_from('<HH',scan, offset)     
                az = head[1]/100.;
                #print("AZ = {:f}, dAZ = {:f}".format(az,d_az) )
                #todo - interpolate az!!!
                offset += 4;
                if (old_az >= 0):
                    d_az = az-old_az;
                old_az = az;
                dd_az = d_az/VLP16_BLOCK_TDURATION * VLP16_DSR_TOFFSET;
                
                for fire in range(VLP16_FIRINGS_PER_BLOCK):
                    arr = struct.unpack_from('<'+'HB'*VLP16_SCANS_PER_FIRING,
                                             scan,offset);
                    #print(arr)
                    point_az = az;
                    point_ts = firing_ts;
                    for  laser_id in range (VLP16_SCANS_PER_FIRING):
                        distance = arr[laser_id*2] * DISTANCE_RESOLUTION;
                        intensity = arr[laser_id*2+1];
                        point_az += dd_az;
                        if (point_az > 360):
                            point_az -= 360;
                        omega = LASER_ANGLES[laser_id] * np.pi / 180.0
                        point_ts += VLP16_DSR_TOFFSET_NS;
                        point = dict(zip(point_keys,(point_az, distance, 
                                                     intensity, omega, point_ts)))
                        points.append(point)
                       
                    offset = offset + VLP16_SCANS_PER_FIRING*RAW_SCAN_SIZE;
                    az += d_az/2;
                    if (az > 360):
                        az -= 360;
                    firing_ts += VLP16_FIRING_TOFFSET_NS

            #tail=struct.unpack_from('<IH', scan, offset)
            #print("{:d} {:d} {:X}".
            #      format(offset,tail[0], tail[1]))
            packet_cnt = packet_cnt + 1
            print(packet_cnt)
    return points, packet_cnt        
            
    
#%%
    

def save_csv(path, data):
    with open(path, 'w') as fp:
        wr = csv.writer(fp, delimiter=',')
        wr.writerows(data)

def calc(dis, azimuth, laser_id, timestamp):
    R = dis * DISTANCE_RESOLUTION
    omega = LASER_ANGLES[laser_id] * np.pi / 180.0
    alpha = azimuth / 100.0 * np.pi / 180.0
    X = R * np.cos(omega) * np.sin(alpha)
    Y = R * np.cos(omega) * np.cos(alpha)
    Z = R * np.sin(omega)
    return [X, Y, Z, timestamp]

def unpack(dirs):
    files = glob.glob(dirs + '/*.bin')
    points = []
    scan_index = 0
    prev_azimuth = None
    for x in files:
        d = open(x, 'rb').read()
        n = len(d)
        for offset in xrange(0, n, 1223):
            ts = d[offset : offset + 17]
            data = d[offset + 17 : offset + 1223]
            print (ts, len(data))
            timestamp, factory = struct.unpack_from("<IH", data, offset=1200)
            assert factory == 0x2237, hex(factory)  # 0x22=VLP-16, 0x37=Strongest Return
            timestamp = float(ts)
            seq_index = 0
            for offset in xrange(0, 1200, 100):
                flag, azimuth = struct.unpack_from("<HH", data, offset)
                assert flag == 0xEEFF, hex(flag)
                for step in xrange(2):
                    seq_index += 1
                    azimuth += step
                    azimuth %= ROTATION_MAX_UNITS
                    if prev_azimuth is not None and azimuth < prev_azimuth:
                        file_fmt = os.path.join(dirs, '%Y-%m-%d_%H%M')
                        path = datetime.now().strftime(file_fmt)
                        try:
                            if os.path.exists(path) is False:
                                os.makedirs(path)
                        except Exception as e:
                            print (e)
                        if not points:
                            timestamp_str = '%.6f' % time.time()
                        else:
                            timestamp_str = '%.6f' % points[0][3]
                        csv_index = '%08d' % scan_index
                        save_csv("{}/i{}_{}.csv".format(path, csv_index, timestamp_str), points)
                        logger.info("{}/i{}_{}.csv".format(path, csv_index, timestamp_str))
                        scan_index += 1
                        points = []
                    prev_azimuth = azimuth
                    # H-distance (2mm step), B-reflectivity (0
                    arr = struct.unpack_from('<' + "HB" * 16, data, offset + 4 + step * 48)
                    for i in xrange(NUM_LASERS):
                        time_offset = (55.296 * seq_index + 2.304 * i) / 1000000.0
                        if arr[i * 2] != 0:
                            points.append(calc(arr[i * 2], azimuth, i, timestamp + time_offset))

#%%                            
def save_package(dirs, data_queue):
    try:
        if os.path.exists(dirs) is False:
            os.makedirs(dirs)
        cnt = 0
        fp = None
        while True:
            if data_queue.empty():
                pass
            else:
                msg = data_queue.get()
                data = msg['data']
                ts = msg['time']
                print (ts, len(data), 'queue size: ', data_queue.qsize(), cnt)
                if fp == None or cnt == 1000000:
                    if fp != None:
                        fp.close()
                    file_fmt = os.path.join(dirs, '%Y-%m-%d_%H%M')
                    path = str(datetime.now().strftime(file_fmt)) + '.bin'
                    logger.info('save to' + path)
                    print ('save to ', path)
                    fp = open(path, 'ab')
                    cnt = 0
                cnt += 1
                fp.write('%.6f' % ts)
                fp.write(data)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        if fp != None:
            fp.close()

def capture(port, data_queue):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind(('', port))
    try:
        while True:
            try:
                data = soc.recv(2000)
                if len(data) > 0:
                    assert len(data) == 1206, len(data)
                    data_queue.put({'data': data, 'time': time.time()})
            except Exception as e:
                print( dir(e), e.message, e.__class__.__name__)
                traceback.print_exc(e)
    except KeyboardInterrupt as e:
        print (e)


if __name__ == "__main__":
    p,n=read_velo_file('E:\\Data\\Voxels\\201804\\spb-50-0\\velodyne_packets\\')

"""    
    if len(sys.argv) < 3:
        print (__doc__)
        sys.exit(2)
    if sys.argv[1] == 'read':
        top_dir = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        processA = Process(target = capture, args = (PORT, DATA_QUEUE))
        processA.start()
        processB = Process(target = save_package, args = (sys.argv[2] + '/' + top_dir, DATA_QUEUE))
        processB.start()
    else:
        unpack(sys.argv[2])
"""
