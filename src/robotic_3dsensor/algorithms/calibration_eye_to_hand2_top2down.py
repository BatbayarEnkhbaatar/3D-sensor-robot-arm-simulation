import numpy as np
import json 


def get_tool_pose(sensor_pose):



  h_matrix_lower= [
      # home pose : p[-0.33569, -0.13998, 0.61284, 2.832, 2.856, -2.203], a=1.0, v=0.25)

   [0.9988,    0.0090  , -0.0481 ,  67.3678],
   [0.0211,   -0.9658  ,  0.2583 , 375.4636],
   [-0.0442,   -0.2590 ,  -0.9649 , 828.8153],
   [     0,         0,         0 ,   1.0000]

    ]

  end_effector_pose = np.dot(h_matrix_lower, sensor_pose)
  end_effector_pose= end_effector_pose.flatten().tolist()

  return end_effector_pose

