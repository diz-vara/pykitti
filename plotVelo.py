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
    fwlim = 60
    backlim = -10
    leftlim = -12
    rightlim = 12
    
    
    stp = step or 100
    if (do3d):
        ax1_3d.cla()
        ax1_3d.axis([leftlim,rightlim,backlim,fwlim])

    ax1.cla()
    ax1.axis([leftlim,rightlim,backlim,fwlim])
    
    v = dataset.velo[pnt][::-1]

    #invertered x-axis!!
    left = v[:,1] < -leftlim
    right = v[:,1] > -rightlim
    back = v[:,0] > backlim
    fw = v[:,0] < fwlim
    
    
    high = v[:,2] > -thr
    hup = v[:,2] < 1
    high = high & left & right & back & fw & hup
    numPoints = v.shape[0]
    idx = np.arange(0,numPoints)[high]

    r = range(0, idx.size, stp)
    h = idx[r]

    ax1.scatter(v[h, 1]*(-1),
                v[h, 0],
                #dataset.velo[pnt][h, 2],
                c=v[h, 2]*50,
                cmap='jet')
    

    if (do3d):
        ax1_3d.scatter(v[h, 1]*(-1),
                    v[h, 0],
                    v[h, 2],
                    c=v[h, 2]*50,
                    cmap='jet')
    else:
        ax4.imshow(dataset.gray[pnt].left,cmap='gray')
    
    if (hasattr(dataset,'rgb')):
        ax2.imshow(dataset.rgb[pnt].left)
        ax3.imshow(dataset.rgb[pnt].right)
    elif (hasattr(dataset,'gray')):
        ax2.imshow(dataset.gray[pnt].left,cmap='gray')
        ax3.imshow(dataset.gray[pnt].right,cmap='gray')
        
    plt.show()
