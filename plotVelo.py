# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:00:27 2016

@author: avarfolomeev
"""
import numpy as np
import matplotlib.pyplot as plt



def plot_velo(pnt,step=100, thr = 3, do3d = False):
    #f2 = plt.figure()
    #ax2 = f2.add_subplot(111, projection='3d')
    fwlim = 15
    backlim = -10
    leftlim = -15
    rightlim = 15
    
    
    stp = step or 100
    if (do3d):
        ax4 = f2.add_subplot(326,projection='3d')
    else:
        ax4 = f2.add_subplot(326)
    ax4.cla()    
        #ax1_3d.axis([leftlim,rightlim,backlim,fwlim])

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
    high = high & left & right & back & hup
    numPoints = v.shape[0]
    idx_all = np.arange(0,numPoints);


    #without fw limit
    idx0 = idx_all[(v[:,0] > 4) & (v[:,1] > -10) & (v[:,1] < 10) & (v[:,2] > -2.5)]
    

    high = high & fw;
    idx = idx_all[high]


    ax1.scatter(v[idx, 1]*(-1),
                v[idx, 0],
                #dataset.velo[pnt][h, 2],
                c=v[idx, 2]*50,
                cmap='jet',
                marker='.',
                edgecolors='face')
    
    leftlim=-4
    rightlim=4
    fwlim = 11
    backlim=4

    left = v[:,1] < -leftlim
    right = v[:,1] > -rightlim
    back = v[:,0] > backlim
    fw = v[:,0] < fwlim
 
    h = v[:,2] > -thr 
    hu = v[:,2] < -1.5

    h = h & hu & left & right & back & fw
    numPoints = v.shape[0]
    patch_idx = np.arange(0,numPoints)[h]
    ax4.cla()
    if (do3d):
        ax4.scatter(v[patch_idx, 1]*-1,
                1.-4./v[patch_idx, 0],
                v[patch_idx, 2]+1.73,
                c=v[patch_idx, 2]+1.73,
                cmap='jet',
                marker='.',
                edgecolors='face')
    else:
        ax4.scatter(v[patch_idx, 1]*-1,
                1.-4./v[patch_idx, 0],
                #v[idx, 2],
                c=v[patch_idx, 2]+1.73,
                cmap='jet',
                marker='.',
                edgecolors='face')
        
        #ax4.imshow(dataset.gray[pnt].left,cmap='gray')
    
    if (hasattr(dataset,'rgb')):
        img = dataset.rgb[pnt].left
        ax2.imshow(img)
        ax3.imshow(dataset.rgb[pnt].right)
    elif (hasattr(dataset,'gray')):
        ax2.imshow(dataset.gray[pnt].left,cmap='gray')
        ax3.imshow(dataset.gray[pnt].right,cmap='gray')
        
    plt.show()
    return v[idx0], img