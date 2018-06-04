# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 16:41:03 2018

@author: avarfolomeev
from https://www.learnopencv.com/rotation-matrix-to-euler-angles/
"""
import math

def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

    
def rotationMatrixToEulerAngles(R) :

    assert(isRotationMatrix(R))

    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])

    singular = sy < 1e-6

    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return np.array([x, y, z])

# Calculates Rotation Matrix given euler angles. [rpy]
def eulerAnglesToRotationMatrix(theta) :
     
    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])
         
         
                     
    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])
                 
    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])
                     
                     
    R = np.dot(R_z, np.dot( R_y, R_x ))
 
    return np.matrix(R)
    

def remove_yaw(rm):
    eul = rotationMatrixToEulerAngles(rm);
    angle = [0,0, 0-eul[2]];

    return (rm * eulerAnglesToRotationMatrix(angle));


# Inputs:
#  road_to_velo - what I've measured on the road
#  imu -        - IMU rotation for that frame      
def get_imu_to_velo_rotation(world_to_velo, world_to_imu):
    world_to_velo_no_yaw = remove_yaw(world_to_velo);
    world_to_imu_no_yaw = remove_yaw(world_to_imu);
    imu_to_velo = (world_to_velo_no_yaw.transpose() * world_to_imu_no_yaw).transpose()
    return imu_to_velo;
    
