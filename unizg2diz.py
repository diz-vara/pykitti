# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 17:05:49 2018

@author: avarfolomeev
"""

labels_unizg = [
    #       name                diz_id    color
    sLabel(  'unlabeled'      ,  0 , (  0,  0,  0) ),  #
    sLabel(  'sky'            ,  1 , ( 128,128,128) ),  #
    sLabel(  'road'           ,  2 , (128, 64, 128) ),
    sLabel(  'sidewalk'       ,  3 , (  0,  0, 192) ),
    sLabel(  'Vegetation'     ,  7 , (128,128,   0) ), #7
    sLabel(  'Building'       ,  8 , (128,  0,   0) ), #8
    sLabel(  'Fence'          , 10 , ( 64, 64, 128) ), #10
    sLabel(  'Pole'           , 10 , (192,192, 128) ), #10
    sLabel(  'Sign'          ,  11 ,  (192,128, 128) ), #11
    sLabel(  'Transport'      , 13 , ( 64,  0, 128) ), #13
    sLabel(  'Pedestrian'     , 14 , ( 64, 64,  0) ), #14
    sLabel(  'Rider'          , 15 , (  0,128, 192) ) #15
]

colors_unizg = np.array([label.color for label in labels_unizg]).astype(np.uint8)


def unizg2diz(base_dir, in_dir, out_dir):
    
    in_dir = os.path.join(base_dir, in_dir)
    out_dir = os.path.join(base_dir, out_dir)

    try:
        os.makedirs(out_dir)
    except:
        pass


    print('Loading masks from ' + in_dir)

    
    

    im_files = sorted(os.listdir(in_dir))
    cnt = 0
    end_string = ' from ' + str(len(im_files))
    
    
    
    
    
    for label_file in im_files:
        print(str(cnt) + end_string)
        cnt = cnt+1
        colors_in = cv2.imread(os.path.join(in_dir, label_file))
        colors_in = cv2.cvtColor(colors_in,cv2.COLOR_RGB2BGR)
        
        
        
        sh = colors_in.shape

        label = np.zeros ((sh[0], sh[1]), dtype = np.uint8)

        
        for idx in range(len(colors_unizg)):
            color = colors_unizg[idx]
            s = (colors_in == color).all(axis=2)
            label[s] = labels_unizg[idx][1]            
        
        cv2.imwrite(os.path.join(out_dir, label_file), label)
