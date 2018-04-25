# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:39:28 2018

@author: avarfolomeev
"""
import struct
from collections import namedtuple
from glob import glob
import os.path


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
    return IMUdata;
     
def extract_position(IMUdata):
    bFix = np.array([d['bFix'] for d in IMUdata])==1;
    bImu = np.array([d['bIMU'] for d in IMUdata])==1;
    bFix = bFix & bImu;                
    Lat = np.array([d['Lat'] for d in IMUdata[bFix]]);
    Lon = np.array([d['Lon'] for d in IMUdata[bFix]]);
    Alt = np.array([d['Alt'] for d in IMUdata[bFix]]);
    return Lat,Lon,Alt
    
def extract_linax(IMUdata):
    bFix = np.array([d['bFix'] for d in IMUdata])==1;
    bImu = np.array([d['bIMU'] for d in IMUdata])==1;
    bFix = bFix & bImu;                
    Lat = np.array([d['Lat'] for d in IMUdata[bFix]]);
    Lon = np.array([d['Lon'] for d in IMUdata[bFix]]);
    Alt = np.array([d['Alt'] for d in IMUdata[bFix]]);
    return Lat,Lon,Alt

    

     