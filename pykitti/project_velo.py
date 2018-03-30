# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 12:34:46 2017

@author: avarfolomeev
"""

import numpy as np

def prepare_velo_points(pts3d_raw):
    '''Replaces the reflectance value by 1, and tranposes the array, so
       points can be directly multiplied by the camera projection matrix'''

    pts3d = pts3d_raw

    numPoints = pts3d.shape[0]
    idx_all = np.arange(0,numPoints);


    idx0 = idx_all[(pts3d[:,0] > 0) & (pts3d[:,1] > -50) & (pts3d[:,1] < 50) 
                    & (pts3d[:,2] > -2.5)]    

    pts3d = pts3d[idx0,:]
    #pts3d[:,3] = 0
    return pts3d.transpose(), idx0

def project_velo_points_in_img(pts3d, T_cam_velo, Rrect, Prect):
    '''Project 3D points into 2D image. Expects pts3d as a 4xN
       numpy array. Returns the 2D projection of the points that
       are in front of the camera only an the corresponding 3D points.'''

    # 3D points in camera reference frame.
    pts3d_cam = Rrect.dot(T_cam_velo.dot(pts3d))

    # Before projecting, keep only points with z>0 
    # (points that are in fronto of the camera).
    #idx = (pts3d_cam[2,:]>=0)
    pts2d_cam = Prect.dot(pts3d_cam)

    return pts2d_cam/pts2d_cam[2,:]
