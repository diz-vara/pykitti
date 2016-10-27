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
basedir='e:/data/datasets/kitti'
date = '2011_09_26'
drive = '0059'
frame_range = range(0, 100, 1)
dataset = pykitti.raw(basedir, date, drive, frame_range)
dataset.load_gray()
dataset.load_velo()
dataset.load_rgb()




#runfile('plotVelo.py')
