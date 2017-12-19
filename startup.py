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
basedir='F:/Datasets/kitti'
date = '2011_09_26'
drive = '0117'
frame_range = range(0, 650, 1)
dataset = pykitti.raw(basedir, date, drive, frame_range)
#dataset.load_gray()
dataset.load_velo()
dataset.load_rgb()
dataset.load_calib()

Prect = dataset.calib.P_rect_20;
Rrect = dataset.calib.R_rect_20;
T_cam_velo = dataset.calib.T_cam2_velo;





runfile('plotVelo.py')
runfile('setFigure.py')