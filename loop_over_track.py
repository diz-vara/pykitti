# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 13:50:19 2017

@author: avarfolomeev
"""
import os

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pykitti
import cv2
import labels

os.chdir('D:/Work/KITTI/pykitti')

#%%
basedir='F:/Datasets/kitti'
date = '2011_10_03'
drive = '0027'
Marks = True
base=0
frame_range = None; #range(base,4544) #None; #range(base,base+2000)#total 4544
dataset = pykitti.raw(basedir, date, drive, frame_range)
#dataset.load_gray()
dataset.load_velo()
dataset.load_rgb()
dataset.load_calib()
dataset.load_Croad()

Prect = dataset.calib.P_rect_20;
Rrect = dataset.calib.R_rect_20;
T_cam_velo = dataset.calib.T_cam2_velo;

#%%

veloTdir = os.path.join(basedir,date,dataset.drive,'velorgbTcsm')

try:
    os.makedirs(veloTdir)
except:
    pass

npoints = dataset.get_velo_num();

for i in range(npoints):
    print (dataset.drive,i,'from',npoints)
    filename = "{:010d}.velorgbTcs".format(i+base)
    filepath = os.path.join(veloTdir,filename)
    v,c = pykitti.overlay_velo(dataset,i, Marks)

    pykitti. save_velo_color(v,c,filepath)