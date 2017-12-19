# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:09:02 2017

@author: avarfolomeev
"""

minx= min(v[:,0])
maxx = max(v[:,0])
miny = min(v[:,1])
maxy = max(v[:,1])

szx = int(np.ceil((maxx-minx)*10))
szy = int(np.ceil((maxy-miny)*10))

zz = np.ones((szx, szy),dtype=np.float32)* (np.nan)

for p in v:
    _x = int ((maxx-p[0])*10)
    _y = int ((maxy-p[1])*10)
    zz[_x,_y] = p[2]+1.73 #velodyne height
