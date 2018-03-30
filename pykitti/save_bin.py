# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:30:34 2017

@author: avarfolomeev
"""

import struct
import numpy as np

def save_velo_color(v, color, name):
    buff = np.zeros(v.shape[0]*v.shape[1]*4,np.uint8)
    npoints = v.shape[0]
    
    ci=color[::-1]
    vi=v[::-1]
    for i in range(npoints):
        p = vi[i,:]
        c = ci[i,:]
        struct.pack_into('fffBBBB',buff,i*16,p[0],p[1],p[2],c[0],c[1],c[2],c[3])
    
        
        
    newFile = open(name, "wb")
        
    newFile.write(buff)
    newFile.close();


