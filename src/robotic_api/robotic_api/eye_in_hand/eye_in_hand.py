
import numpy as np
from scipy.spatial.transform import Rotation as Rot
import eye_in_hand_functions_used as eye_in_hand


T_CT = [] #Camera Target Coordinate
T_BG = [] #Robot Coordinate


T_CT = np.array([
 -55.9,  -59.2 , 550.25 ,  0,    -0,     0,  
        ], dtype=float)
T_BG = np.array([
527.642,-67.951,324.800,-179.0725,-0.7903,124.4395,
        ], dtype=float)

T_GC = np.array([
          [-0.71367864602094,0.688018386580514,0.131504714519533,-115.588880567787],
          [-0.690563696712456,-0.722539072731587,0.0325433427755276,-17.1267407623769],
          [0.117407712679131,-0.0675868929846909,0.990781227567484,116.887298968635],
          [0,0,0,1]
        ], dtype=float)


estimated_pose = eye_in_hand.compute_target_pose_base_mm_deg(T_CT,T_BG,T_GC)
# print("The estimated pose with extrinsic is :", estimated_pose)

tool_pose = eye_in_hand.wrist_to_tool_pose6(estimated_pose, L=205, sX=-30, sY=-10)
# print("The estimated tool pose is :", tool_pose)