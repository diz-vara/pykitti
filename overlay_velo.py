# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:36:31 2017

@author: avarfolomeev
"""


def overlay_velo(pnt):
    v,img=plot_velo(pnt, thr=2, step=1, do3d=False)
    v_prep = prepare_velo_points(v)
    v_proj = project_velo_points_in_img(v_prep, T_cam_velo, Rrect, Prect)
    plt.cla()
    vmin = min(v_proj[0][2])
    plt.scatter(v_proj[1][0,:], v_proj[1][1,:], 
                c=v_proj[0][2], 
                vmax = -1.23, vmin = -1.73,
                marker = '.', edgecolors='face')
    plt.imshow(img)    
    