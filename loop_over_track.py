# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 13:50:19 2017

@author: avarfolomeev
"""
import os


#%%
basedir='F:/Datasets/kitti'
date = '2011_09_26'
drive = '0051'
base=0
frame_range = None #range(base,base+1543)
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

veloTdir = os.path.join(basedir,date,dataset.drive,'velorgbTcs')

try:
    os.makedirs(veloTdir)
except:
    pass

npoints = len(dataset.velo)

for i in range(npoints):
    print (dataset.drive,i,'from',npoints)
    filename = "{:010d}.velorgbTcs".format(i+base)
    filepath = os.path.join(veloTdir,filename)
    v,c = overlay_velo(i)
    save_velo_color(v,c,filepath)