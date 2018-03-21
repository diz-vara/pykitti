# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:36:31 2017

@author: avarfolomeev
"""

import scipy.misc
import matplotlib.pyplot as plt
import PIL.Image as Image

def threshold_image(image, thresh=25, kernel = 25):
    
    red_channel = image[:,:,0];
   
    blurred = cv2.medianBlur(red_channel,kernel);
    diff = cv2.subtract(red_channel, blurred)
    thr = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)[1];
    out = cv2.medianBlur(thr,3)
    #out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))

    return out


def overlay_mask(img, gt):
    road_color = 7 #np.array([1, 0, 1])
    gt_road = np.all(gt == road_color)
    gt_road = gt_road.reshape(*gt_road.shape, 1)
    
    #todo: assign 'road' attribute to the v voxels that are 
    #   at points with gt_road == True
    
    
    #road_mask = np.dot(gt_road, np.array([[0, 255, 0, 127]]))
    #road_mask = scipy.misc.toimage(road_mask, mode="RGBA")
    
    street_im = scipy.misc.toimage(img)
    #street_im.paste(road_mask, box=None, mask=road_mask)
    return street_im , gt_road
        
    
def overlay_cs(pnt):
    plt.imshow(dataset.rgb[pnt].left)
    plt.imshow(Image.fromarray(colors[dataset.road[pnt]]))

    
#returns results in npoins by 4 byte array, 4th byte is for type
# first 3 bytes - color of the point
def overlay_velo(pnt, marks = True):
    v = dataset.velo[pnt][::-1]
    img = dataset.rgb[pnt].left
    img_u8 = (img*255).astype(np.uint8)
    
    
    mask =  dataset.road[pnt].copy()
    #mask = cv2.medianBlur(mask,3)
    
    img_u8 = cv2.medianBlur(img_u8,7)
    thr = threshold_image(img_u8,27)
    
    #road marking - 20 (traffic sign) - was type 65
    if (marks):
        mask[mask==7 & thr] = 65

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


    #plot_velo(v, img, mask, thr=2, do3d=False)


    #results array, 4th byte is for type
    #cmask = colors[mask]
    colored = np.zeros((npoints,4),dtype=np.uint8)
    

    for i in range(len(idx_inside)):
        p = v_inside[i];
        ii = idx_inside[i];
        colored[ii,:3] = img_u8[p[1],p[0]]; #(cmask[p[1],p[0]])
        voxel_class = mask[p[1],p[0]];
        '''if (voxel_class == 65): 
            if (v[ii,3] < 0.25):
                voxel_class = 7;
            else:
                voxel_class = 20;
        '''        
        colored[ii,3] = voxel_class;

    '''
    ax1.scatter(v[idx_inside, 1]*(-1),
                v[idx_inside, 0],
                c=(colored[idx_inside]).astype(np.float32)/255, 
                marker=',',
                edgecolors='face',
                s=40, alpha = 0.4);
    '''
    

    
    if ('ax' in globals() and ax is not None):
        ax.cla()
        ax.scatter(v_proj[inside,0], v_proj[inside,1], 
                    c=colored[idx_inside,:3]/255, 
                    vmax = -1.23, vmin = -1.73,
                    marker = '.', edgecolors='face',
                    s = 30, alpha = 0.4)
        #ax.imshow(street_im)    

    return v,colored
    
    
    