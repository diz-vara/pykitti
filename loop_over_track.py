# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 13:50:19 2017

@author: avarfolomeev
"""




npoints = len(dataset.velo)

for i in range(npoints):
    print (i,'from',npoints)
    filename = "{:010d}.velorgbT".format(i)
    filepath = os.path.join(basedir,date,dataset.drive,'velorgbT',filename)
    v,c = overlay_velo(i)
    save_velo_color(v,c,filepath)