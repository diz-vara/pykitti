# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:39:28 2018

@author: avarfolomeev
"""
import struct
from collections import namedtuple
from glob import glob
import os.path
import numpy as np
import matplotlib.pyplot as plt

from pyquaternion import Quaternion
import math


def unpack_IMUdata(data):
    keys = [
    'bIMU', 'bFix', 'bTwist', 'bTimeRef', 
    'ts_s', 'ts_ns',
    'Qx', 'Qy', 'Qz', 'Qw',
    'AVx', 'AVy',  'AVz', 
    'LAx', 'LAy', 'LAz',
    'Lat', 'Lon',  'Alt', 
    'TwLx', 'TwLy', 'TwLz', 
    'TwAx', 'TwAy', 'TwAz', 
    'Tref_s', 'Tref_ns']
    a = struct.unpack('BBBBiixxxxdddddddddddddddddddii',data);
    d = dict(zip(keys,a));

    if (not d['bFix']):
        d['Lat'] = d['Lon'] = d['Alt'] = None;

    if (not d['bIMU']):
        d['Qx'] = d['Qy'] = d['Qz'] = d['Qw'] = None;
        d['AVx'] = d['AVy'] =  d['AVz'] = None; 
        d['LAx'] = d['LAy'] = d['LAz'] = None;

    if (not d['bTwist']):
        d['TwLx'] = d['TwLy'] = d['TwLz'] = None; 
        d['TwAx'] = d['TwAy'] = d['TwAz'] = None; 

    if (not d['bTimeRef']):
        d['Tref_s'] = d['Tref_ns'] = None;
        
    return d

    
    
def read_IMUdata(path):  
    imu_path = os.path.join(path, '*.imu');

    imu_files = sorted(glob(imu_path));

    IMUdata = [];
    for fname in imu_files:
        data = np.fromfile(fname,dtype=np.int8);
        IMUdata.append(unpack_IMUdata(data));

    return IMUdata;
  
def read_IMUfile(filename):  

    RECORDSIZE = 176 
    IMUdata = [];
    filesize = os.path.getsize(filename);
    nrecords = filesize//RECORDSIZE;
    
    file = open(filename,'rb')
    

    for i in range(nrecords):
        data = np.fromfile(file,dtype=np.int8,count=RECORDSIZE);
        IMUdata.append(unpack_IMUdata(data));
    file.close();
    return np.array(IMUdata);
     
def extract_position(IMUdata):
    bFix = np.array([d['bFix']==1 and d['bIMU'] == 1  for d in IMUdata]);
    Pos = [(d['Lat'], d['Lon'], d['Alt']) for d in IMUdata[bFix]];
    return np.array(Pos)
    
def extract_linacc(IMUdata):
    bFix = np.array([d['bFix']==1 and d['bIMU'] == 1  for d in IMUdata]);
    acc = [(d['LAx'], d['LAy'], d['LAz']) for d in IMUdata[bFix]];
                  
    return np.array( acc )
    
def extract_quaternion(IMUdata):
    bFix = np.array([d['bFix']==1 and d['bIMU'] == 1  for d in IMUdata]);
    Q = [Quaternion(d['Qw'], d['Qx'], d['Qy'], d['Qz']) for d in IMUdata[bFix]]
    return np.array( Q )
    
def extract_ts(IMUdata):
    bFix = np.array([d['bFix']==1 and d['bIMU'] == 1  for d in IMUdata]);
    ts = np.array([(d['ts_s'],d['ts_ns']) for d in IMUdata[bFix]]);
    return np.array( ts )

#only linear - there were no angle velocities :(    
def extract_twist(IMUdata):
    bTwist = np.array([d['bTwist']==1 for d in IMUdata]);

    twL = [(d['TwLx'],d['TwLy'],d['TwLz']) for d in IMUdata[bTwist]];
    return np.array(twL)
    
    
#утащил из википедии    
def quaternion_to_euler_angle(w, x, y, z):
	ysqr = y * y
	
	t0 = +2.0 * (w * x + y * z)
	t1 = +1.0 - 2.0 * (x * x + ysqr)
	X = math.degrees(math.atan2(t0, t1))
	
	t2 = +2.0 * (w * y - z * x)
	t2 = +1.0 if t2 > +1.0 else t2
	t2 = -1.0 if t2 < -1.0 else t2
	Y = math.degrees(math.asin(t2))
	
	t3 = +2.0 * (w * z + x * y)
	t4 = +1.0 - 2.0 * (ysqr + z * z)
	Z = math.degrees(math.atan2(t3, t4))
	
	return (X, Y, Z)
    

def extract_euler(IMUdata):
    bFix = np.array([d['bFix']==1 and d['bIMU'] == 1  for d in IMUdata]);
    e = [quaternion_to_euler_angle(d['Qw'], d['Qx'], d['Qy'], d['Qz']) for d in IMUdata[bFix]]
    return np.array( e )
     