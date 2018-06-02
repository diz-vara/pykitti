# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:42:11 2018

@author: avarfolomeev
"""

cmap = ['blue','dodgerblue','cyan', 'lightgreen', 'green', 'yellow', 
        'orange', 'red', 'magenta', 'brown',  'darkgray'];
        
        
draw3d = False
start = 420

a2.cla()

ff = np.arange(start,start+22,1)


filter_h = (ptR1_11_12[:,2] > -1.4) & (ptR1_11_12[:,2] < 1.1)

if (draw3d):
    a3.cla()


    
for frame in ff:
    filter_frame = (fR1_11_12==frame)
    a2.scatter(ptR1_11_12[filter_frame & filter_h,0], 
               ptR1_11_12[filter_frame & filter_h,1],
               marker='.',
               edgecolors='face',
               color=cmap[(frame-start)%11],s=1)
    a2.scatter(nR1_11_12[filter_frame,0], 
               nR1_11_12[filter_frame,1],marker='x',
               edgecolors='face',
               color=cmap[(frame-start)%11],s=16)

    if (draw3d):
        a3.scatter(0-ptR1_12[filter_frame,0], 
                   ptR1_12[filter_frame,1],
                   ptR1_12[filter_frame,2],
                   marker='.',edgecolors='face',color=cmap[frame%11],s=1)
    
        a3.scatter(0-nR1_12[filter_frame,0], 
                   nR1_12[filter_frame,1],
                   nR1_12[filter_frame,2],
                   marker='.',edgecolors='face',color=cmap[frame%11],s=3)
    
 #%%
if (False):
 for frame in ff:
    filter_frame = (fR1_11==frame)
    a3.scatter(ptR1_11[filter_range & filter_frame,0], 
               ptR1_11[filter_range & filter_frame,1],
               ptR1_11[filter_range & filter_frame,2],
               marker='.',edgecolors='face',color=cmap[frame%11],s=5)       