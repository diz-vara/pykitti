# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 17:07:12 2016

@author: avarfolomeev
"""

#do it from command line!!!
#%matplotlib

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pykitti
import cv2
import numpy as np
#%%
basedir='F:/Datasets/kitti'
date = '2011_09_26'
drive = '0106'
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

#%matplotlib qt5


runfile('plotVelo.py')
runfile('setFigure.py')