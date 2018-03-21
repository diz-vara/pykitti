# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 17:21:05 2018

@author: avarfolomeev
"""

imageV0 = cv2.imread('E:\\Data\\CN\\video\\IMU\\2017_11_08\\o\\2017_11_08_06_48_44\\2017_11_08_06_48_44_001017.jpg ')

imageVu = cv2.undistort(imageV0, mtx, dist, None, mtx)
cv2.imwrite("nicigo-vertical-undistorted.png",imageVu)

#o, lines = detectLanes(image,mode)
#height = image.shape[0]
#%%
src = np.float32(
   [[ 982, 461], [ 989, 391], 
    [1132, 520], [1136, 410]])

down = 0.3
height = 0.8
d0 = 17
distance = 7.12
top = 10
far = 100

scale = 50 # pixel per m
#
dst = np.float32(
   [[ far-(d0+distance), top-down], [ far-(d0+distance), top-(down+height) ], 
    [  far-d0, top - down],   [ far-d0, top-(down+height)]])

Mv = cv2.getPerspectiveTransform(src, dst * scale)   #/100 - 10 cm per pixel
Mvinv = cv2.getPerspectiveTransform(dst* scale, src)

            # e) use cv2.warpPerspective() to warp your image to a top-down view
wv = cv2.warpPerspective(imageVu, M, (int(far * scale), int(10 * scale)), 
                             flags=cv2.INTER_LINEAR)

plt.imshow(wv)
cv2.imwrite("nicigo-warped0vertical.png",wv)

pickle.dump((Mv, Mvinv), open("nicigo-Mv.p", "wb"))

#%%

image_1_name = 'E:\\Data\\CN\\IMU\\20171108\\2017_11_08_06_30_40_000168.jpg'
image_1 = cv2.imread(image_1_name)
image_1_u = cv2.undistort(image_1, mtx, dist, None, mtx)

image_1_vw = cv2.warpPerspective(image_1_u, Mv, (far  * scale, 
                                               20 * scale ), 
                             flags=cv2.INTER_LINEAR)
plt.imshow(image_1_vw)
cv2.imwrite("test-264-v-warped.png",image_1_vw)
ticks = np.arange(5,100,5)
plt.xticks(ticks*scale,far-ticks)


