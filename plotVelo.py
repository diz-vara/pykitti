# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:00:27 2016

@author: avarfolomeev
"""
import numpy as np
import matplotlib.pyplot as plt



def plot_velo(v, img, mask, thr = 3, do3d = False):
    #f2 = plt.figure()
    #ax2 = f2.add_subplot(111, projection='3d')
    fwlim = 35
    backlim = -10
    leftlim = -15
    rightlim = 15
    
    
        #ax1_3d.axis([leftlim,rightlim,backlim,fwlim])

    ax1.cla()
    ax2.cla()    
    ax3.cla()    
    ax4.cla()    
    ax1.axis([leftlim,rightlim,backlim,fwlim])
    

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
    
    ax2.imshow(img)
    gt_ovly, road = overlay_mask(img,mask)
    ax3.imshow(gt_ovly)
        
    plt.show()
    #return v[idx0], img, gt