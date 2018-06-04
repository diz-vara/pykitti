# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:42:11 2018

@author: avarfolomeev
"""

cmap = ['blue','dodgerblue','cyan', 'lightgreen', 'green', 'yellow', 
        'orange', 'red', 'magenta', 'brown',  'darkgray'];
        
        

a1.cla()

cnt = 0
rm = extract_quaternion(imuR01_11[0:2])[0].rotation_matrix
for frame in range(1,11):
    pt_ = [[p['X'], p['Y'], p['Z']] for p in pointsR1_11 if p['frame']==frame]
    ptr = np.array(pt_ * imu_to_velo.transpose() * rm);

    filter_h = (ptr[:,2] > -1.8)
    a1.scatter(ptr[filter_h,0], 
               ptr[filter_h,1],
               marker='.',
               edgecolors='face',
               color=cmap[frame],s=1)
