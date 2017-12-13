# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 17:47:51 2017

@author: avarfolomeev
"""
import pykitti
import cv2
import matplotlib.pyplot as plt

basedir = 'F:/Datasets/KITTI'
date = '2011_09_26'

drive = '0117'
        
data = pykitti.raw(basedir, date, drive, range(0, 5, 1))
data.load_calib()
data.load_oxts()
data.load_rgb()

plt.imshow(data.rgb[0].left)

