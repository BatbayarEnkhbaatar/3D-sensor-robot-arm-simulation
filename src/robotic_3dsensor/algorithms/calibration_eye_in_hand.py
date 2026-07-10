import numpy as np
import json 


def get_tool_pose(sensor_pose):



  h_matrix__eye_in_hand= [
      # home pose : [-133.06 56.25 418.91 3.867 1.684 1.245];
        [0.9962,   -0.0137,   -0.0862, [ -98.31403394]],
        [0.0810,   -0.2244,    0.9711,   -95.9083353],
        [-0.0327,   -0.9744,   -0.2224,  -119.52675638],
        [ 0,         0,         0,    1.0000]

     ]

  end_effector_pose = np.dot(h_matrix__eye_in_hand, sensor_pose)
  end_effector_pose= end_effector_pose.flatten().tolist()

  return end_effector_pose
# print("Get Tools")
# print(get_tool_pose(sensor_pose=sensor_pose))

