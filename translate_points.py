# -*- coding: utf-8 -*-
"""
Created on Thu May 10 12:03:02 2018

@author: avarfolomeev
"""
import numpy as np

def translate_points(points, imu_to_velo_rot, IMUdata,base=None):
    
    out = []
    IMU_idx = -1
    IMU_ts = extract_ts(IMUdata)
    Ref_ts = extract_time_ref(IMUdata)
    pos = extract_position(IMUdata);

    #correctionf for ned:swap ases and reverse x
    ned_corr = np.array( [[0,  1, 0], 
                          [1,  0, 0],
                          [0,  0, 0]]);
    

    imu_to_velo_inv = imu_to_velo_rot.transpose();

    ned = np.dot(lla2ned(pos,base),ned_corr);
    q = extract_quaternion(IMUdata);
    num_ts = len(IMU_ts)
    base = 0;
    times = [];

    qus = []
    diffs = []
    
    pnt = points[0];
    base_velo_time = copy.copy(pnt['ts']);

    while (base_velo_time >= IMU_ts[IMU_idx+1] and IMU_idx < num_ts):
        IMU_idx += 1;
    #this is the end    
    if (IMU_idx >= num_ts) :
        return;

    #IMU_idx -= 1;
    #if (IMU_idx < 0):
    #    IMU_idx = 0;
        
    #IMU_idx -= 1;    
    base_time_ref = Ref_ts[IMU_idx];    


    cnt = 0;
        
    for pnt in points:

        ts = pnt['ts']

        time_ref = ts - base_velo_time + base_time_ref;
        
        while (time_ref > Ref_ts[IMU_idx+1] and IMU_idx < num_ts):
            IMU_idx += 1;
        #this is the end    
        if (IMU_idx >= num_ts) :
            break;
            
        dt = (time_ref - Ref_ts[IMU_idx]).double();
        time_step = (Ref_ts[IMU_idx+1] - Ref_ts[IMU_idx]).double();
        
        d_pos = (ned[IMU_idx+1]-ned[IMU_idx])/time_step*dt;             
        q_int = q[IMU_idx].slerp(q[IMU_idx],q[IMU_idx+1], dt/time_step);                   
        
        pt = np.array([pnt['X'], pnt['Y'], pnt['Z']])
        
        pt = np.dot(pt, imu_to_velo_inv)
        
        if (pt[0] > 0.5) and (pt[0] < 120) and (pt[1] > -25) and (pt[1] < 35) and (pt[2] > -2.8) and (pt[2] < 100.5):
            
            new_point = q_int.rotate(pt) + ned[IMU_idx] + d_pos;
                               
    
            out.append(new_point)
            #out.append(ned[IMU_idx] + d_pos)
            diffs.append(pnt['frame']);
            #diffs.append(pnt['frame']);
            qus.append(ned[IMU_idx]+d_pos);
        cnt += 1;
        if (cnt%1000 == 0):
            print(cnt)
                
            
    #manual zero-az point re-referencing
    ts = ROS_ts(1520430272,617093234);
    time_ref = ts - base_velo_time + base_time_ref;
    IMU_idx = -1;
    while (time_ref > Ref_ts[IMU_idx+1] and IMU_idx < num_ts):
        IMU_idx += 1;

    
    #difference from one step, but I;ll use another ?????
    dt = (time_ref - Ref_ts[IMU_idx]).double();

    IMU_idx -= 2;
    if (IMU_idx < 0):
        IMU_idx = 0;
        
    time_step = (Ref_ts[IMU_idx+1] - Ref_ts[IMU_idx]).double();
    print (IMU_idx,dt,time_step)        
    
    d_pos = (ned[IMU_idx+1]-ned[IMU_idx])/time_step*dt + ned[IMU_idx];             
    q_int = q[IMU_idx].slerp(q[IMU_idx],q[IMU_idx+1], dt/time_step);                   

    
        
    return np.array(out),np.array(qus), np.array(diffs)-1, d_pos, q_int
    
