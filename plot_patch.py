# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 16:59:01 2017

@author: avarfolomeev
"""

leftlim=-3.8
rightlim=3
fwlim = 11
backlim=4

left = v[:,1] < -leftlim
right = v[:,1] > -rightlim
back = v[:,0] > backlim
fw = v[:,0] < fwlim

h = left & right & back & fw
numPoints = v.shape[0]
idx = np.arange(0,numPoints)[h]
ax4.cla()
ax4.scatter(v[idx, 1]*-1,
                v[idx, 0],
                #dataset.velo[pnt][h, 2],
                c=v[idx, 2]*50,
                cmap='jet',
                marker='.',
                edgecolors='face')
