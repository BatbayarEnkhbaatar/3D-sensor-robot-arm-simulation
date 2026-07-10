import numpy as np
import json 


def get_tool_pose(sensor_pose, r_pose):
  h_matrix_upper = [

    #home pose : -0.13297, 0.05558, 0.49863, 4.039, 1.691, 1.626
        [0.9923,   -0.0734,   -0.0998, -117.1474],
        [0.1037,    0.0507,    0.9933,  -19.3610],
        [-0.0678,   -0.9960,    0.0579,  593.9509],
        [0, 0, 0,    1.0000],
  ]
  h_matrix_lower= [

      # home pose : [-133.06 56.25 418.91 3.867 1.684 1.245];
        [0.9962,   -0.0137,   -0.0862, -136.2590],
        [0.0810,   -0.2244,    0.9711,   -3.9675],
        [-0.0327,   -0.9744,   -0.2224,  491.9472],
        [ 0,         0,         0,    1.0000]

    ]
  if r_pose =="lower": 
    end_effector_pose = np.dot(h_matrix_lower, sensor_pose)
    end_effector_pose= end_effector_pose.flatten().tolist()
  else:
    end_effector_pose = np.dot(h_matrix_upper, sensor_pose)
    end_effector_pose= end_effector_pose.flatten().tolist()

  return end_effector_pose
# print("Get Tools")
# print(get_tool_pose(sensor_pose=sensor_pose))

