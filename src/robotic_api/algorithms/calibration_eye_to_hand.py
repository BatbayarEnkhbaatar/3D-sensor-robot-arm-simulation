import numpy as np
import json 


def get_tool_pose(sensor_pose):
    
  h_matrix_lower = [
            [-0.1024,   -0.9946,   -0.0187,  604.5643],
            [-0.9947,    0.1026,   -0.0114, -119.9043],
            [0.0133 ,   0.0174 ,  -0.9998,  404.8987],
            [0,         0,         0,    1.0000]
            ]

  # [[-0.1047, -0.9923,  0.0656,  572.9163],
  #   [-0.9943,  0.1032, -0.0251, -130.9920],
  #   [ 0.0182, -0.0679, -0.9975,  399.4213],
  #   [ 0.0,     0.0,     0.0,       1.0   ]

  #           ]


  end_effector_pose = np.dot(h_matrix_lower, sensor_pose)
  end_effector_pose= end_effector_pose.flatten().tolist()

  return end_effector_pose

