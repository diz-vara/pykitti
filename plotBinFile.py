# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 12:00:27 2016

@author: avarfolomeev
"""
import numpy as np
import matplotlib.pyplot as plt



def plot_file(filename,step=100, thr = 3, do3d = False):
    #f2 = plt.figure()
    #ax2 = f2.add_subplot(111, projection='3d')
    fwlim = 50
    backlim = 0
    leftlim = -5
    rightlim = 5
    
    
    stp = step or 100
    if (do3d):
        ax4 = f2.add_subplot(326,projection='3d')
    else:
        ax4 = f2.add_subplot(326)
    ax4.cla()    
        #ax1_3d.axis([leftlim,rightlim,backlim,fwlim])

    ax1.cla()
    ax1.axis([leftlim,rightlim,backlim,fwlim])
    
    scan = np.fromfile(filename, dtype = np.float32)
    scan=scan.reshape((-1,4))
    v = scan[::-1]

    #invertered x-axis!!
    left = v[:,0] < -leftlim
    right = v[:,0] > -rightlim
    back = v[:,2] > backlim
    fw = v[:,2] < fwlim
    
    
    high = v[:,1] > -thr
    hup = v[:,1] < 10
    high = high & left & right & back & fw & hup
    numPoints = v.shape[0]
    idx = np.arange(0,numPoints)[high]


    ax1.scatter(v[idx, 0]*(-1),
                v[idx, 2],
                #v[idx,1],
                c=v[idx, 1],
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
    hu = v[:,2] < -1.

    h = h & hu & left & right & back & fw
    numPoints = v.shape[0]
    idx = np.arange(0,numPoints)[h]
    ax4.cla()
    if (do3d):
        ax4.scatter(v[idx, 1]*-1,
                v[idx, 0],
                v[idx, 2]+1.73,
                c=v[idx, 2]+1.73,
                cmap='jet',
                marker='.',
                edgecolors='face')
    else:
        ax4.scatter(v[idx, 1]*-1,
                v[idx, 0],
                #v[idx, 2],
                c=v[idx, 2]+1.73,
                cmap='jet',
                marker='.',
                edgecolors='face')
        
        #ax4.imshow(dataset.gray[pnt].left,cmap='gray')
    
        
    plt.show()
    return v[idx,:]