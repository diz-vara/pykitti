# -*- coding: utf-8 -*-
"""
Created on Thu May 10 12:03:02 2018

@author: avarfolomeev
"""
import numpy as np

def translate_points(points, imu_to_velo_rot, IMUdata):
    
    out = []
    IMU_idx = -1
    cnt = 1e6
    IMU_ts = extract_ts(IMUdata)
    Ref_ts = extract_time_ref(IMUdata)
    pos = extract_position(IMUdata);

    #correctionf for ned:swap ases and reverse x
    ned_corr = np.array( [ [0, -1, 0], [1, 0, 0], [0,0,0]]);
    ned = np.dot(lla2ned(pos),ned_corr);
    q = extract_quaternion(IMUdata);
    num_ts = len(IMU_ts)
    base = 0;
    times = [];

    neds = []
    diffs = []
    
    pnt = points[0];
    ts = pnt['ts']

    while (ts >= IMU_ts[IMU_idx+1] and IMU_idx < num_ts):
        IMU_idx += 1;
    #this is the end    
    if (IMU_idx >= num_ts) :
        return;

    base_time_ref = Ref_ts[IMU_idx];    
    base_velo_time = copy.copy(ts);


        
    for pnt in points:

        ts = pnt['ts']

        time_ref = ts - base_velo_time + base_time_ref;
        
        while (time_ref >= Ref_ts[IMU_idx+1] and IMU_idx < num_ts):
            IMU_idx += 1;
        #this is the end    
        if (IMU_idx >= num_ts) :
            break;
        
        pt = np.array([pnt['X'], pnt['Y'], pnt['Z']])
        pt = np.dot(pt, imu_to_velo_rot.transpose())
            
        new_point = np.dot(pt, q[IMU_idx].rotation_matrix) + ned[IMU_idx]

        out.append(new_point)
        diffs.append(IMU_idx)
        neds.append(ned[IMU_idx]);
        cnt = cnt-1
        if (cnt<0):
            break;
                
    return np.array(out),np.array(neds), np.array(diffs)
    
