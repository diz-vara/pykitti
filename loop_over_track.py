# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 13:50:19 2017

@author: avarfolomeev
"""
import os

veloTdir = os.path.join(basedir,date,dataset.drive,'velorgbTcs')

try:
    os.makedirs(veloTdir)
except:
    pass

npoints = len(dataset.velo)

for i in range(npoints):
    print (i,'from',npoints)
    filename = "{:010d}.velorgbTcs".format(i)
    filepath = os.path.join(veloTdir,filename)
    v,c = overlay_velo(i)
    save_velo_color(v,c,filepath)