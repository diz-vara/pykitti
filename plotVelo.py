# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:00:27 2016

@author: avarfolomeev
"""
import numpy as np
import matplotlib.pyplot as plt



def plot_velo(pnt,step=100, thr = 1.5, do3d = False):
    #f2 = plt.figure()
    #ax2 = f2.add_subplot(111, projection='3d')
    
    stp = step or 100
    if (do3d):
        ax1_3d.cla()
        ax1_3d.axis([-15,10,-20,20])
    else:
        ax1.cla()
        ax1.axis([-15,10,-20,20])
    

    high = dataset.velo[pnt][:,2] > -thr
    numPoints = dataset.velo[pnt].shape[0]
    idx = np.arange(0,numPoints)[high]

    r = range(0, idx.size, stp)
    h = idx[r]
    
    if (do3d):
        ax1_3d.scatter(dataset.velo[pnt][h, 1]*(-1),
                    dataset.velo[pnt][h, 0],
                    dataset.velo[pnt][h, 2],
                    c=dataset.velo[pnt][h, 2]*50,
                    cmap='jet')
    else:
        ax1.scatter(dataset.velo[pnt][h, 1]*(-1),
                    dataset.velo[pnt][h, 0],
                    #dataset.velo[pnt][h, 2],
                    c=dataset.velo[pnt][h, 2]*50,
                    cmap='jet')
    
    ax2.imshow(dataset.rgb[pnt].left)
    ax3.imshow(dataset.rgb[pnt].right)
    ax4.imshow(dataset.gray[pnt].left, cmap='gray')
    plt.show()
