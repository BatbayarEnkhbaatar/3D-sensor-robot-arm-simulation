import numpy as np
import json 


def get_tool_pose(sensor_pose):

      # home pose : p[-0.33569, -0.13998, 0.61284, 2.832, 2.856, -2.203], a=1.0, v=0.25)

  h_matrix_lower = [
            [-0.1024,   -0.9946,   -0.0187,  604.5643],
            [-0.9947,    0.1026,   -0.0114, -119.9043],
            [0.0133 ,   0.0174 ,  -0.9998,  404.8987],
             [0,         0,         0,    1.0000]
            ]


  end_effector_pose = np.dot(h_matrix_lower, sensor_pose)
  end_effector_pose= end_effector_pose.flatten().tolist()

  return end_effector_pose

