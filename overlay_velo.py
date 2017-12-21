# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:36:31 2017

@author: avarfolomeev
"""

import scipy.misc
import matplotlib.pyplot as plt


def overlay_mask(img, gt):
    road_color = np.array([1, 0, 1])
    gt_road = np.all(gt == road_color, axis=2)
    gt_road = gt_road.reshape(*gt_road.shape, 1)
    
    #todo: assign 'road' attribute to the v voxels that are 
    #   at points with gt_road == True
    
    
    road_mask = np.dot(gt_road, np.array([[0, 255, 0, 127]]))
    road_mask = scipy.misc.toimage(road_mask, mode="RGBA")
    
    street_im = scipy.misc.toimage(img)
    street_im.paste(road_mask, box=None, mask=road_mask)
    return street_im, gt_road
        
#returns results in npoins by 4 byte array, 4th byte is for type
# first 3 bytes - color of the point
def overlay_velo(pnt):
    v = dataset.velo[pnt][::-1]
    img = dataset.rgb[pnt].left
    mask =  dataset.road[pnt]


    npoints = len(v)
    street_im, gt_road = overlay_mask(img,mask)

    v_prep, idx = prepare_velo_points(v)
    v_proj = project_velo_points_in_img(v_prep, T_cam_velo, 
                                        Rrect, Prect)
    

    mask_h = mask.shape[0]
    mask_w = mask.shape[1]
    
    v_proj = v_proj.transpose()
    
    vp_int = v_proj.round().astype(np.int);
    
    inside =  (vp_int[:,0] >= 0) & (vp_int[:,1] >= 0) 
    inside = inside & (vp_int[:,1] < mask_h) & (vp_int[:,0] < mask_w)
    
    v_inside = vp_int[inside,:]
    idx_inside = idx[inside]    


    plot_velo(v, img, mask, thr=2, do3d=False)


    #results array, 4th byte is for type
    colors = np.zeros((npoints,4),dtype=np.uint8)

    for i in range(len(idx_inside)):
        p = v_inside[i];
        ii = idx_inside[i];
        colors[ii,0:3] = (img[p[1],p[0]]*255).astype(np.uint8);
        if (gt_road[p[1],p[0],0]):
            v[ii,3] = 2;
            colors[ii,3] = 1;
        else:
            v[ii,3] = -1;
            colors[ii,3] = 255;
    b_not_road = (colors[:,3] == 255);
    b_road = (colors[:,3] == 1); 
    
    
    ax1.scatter(v[b_road, 1]*(-1),
                v[b_road, 0],
                c=(colors[b_road]).astype(np.float32)/255, 
                marker=',',
                edgecolors='face',
                s=40, alpha = 0.4);

    ax1.scatter(v[b_not_road, 1]*(-1),
                v[b_not_road, 0],
                c=(colors[b_not_road]).astype(np.float32)/255, 
                marker='o',
                edgecolors='face',s=10, alpha = 0.4);
    

    
    ax.cla()
    ax.scatter(v_proj[:,0], v_proj[:,1], 
                c=v_prep[2], 
                vmax = -1.23, vmin = -1.73,
                marker = '.', edgecolors='face',
                s = 15, alpha = 0.4)
    ax.imshow(street_im)    
    return v,colors
    
    
    