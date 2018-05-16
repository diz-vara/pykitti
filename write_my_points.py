# -*- coding: utf-8 -*-
"""
Created on Tue May 15 14:57:22 2018

@author: avarfolomeev
"""

import os.path
import struct


def save_points(path, points, frames):
    format_4f = 'ffff'
    
    frame_path = os.path.join(path,'frames');
    if os.path.exists(frame_path) is False:
        os.makedirs(frame_path)

    one_file = open(os.path.join(path,'points_out.bin'),'wb')
    for f in range (frames[-1]+1):
        pts = points[frames==f,:]

        fname = os.path.join(frame_path,'{:08d}.bin'.format(f))
        file = open(fname,'wb')
        for pt in pts:
            bf = struct.pack(format_4f,pt[0], pt[1], pt[2], 1.);
            file.write(bf);
            one_file.write(bf);
        file.close();
    one_file.close();

                         