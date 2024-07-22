#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import os
from PIL import Image
import numpy as np
from ament_index_python import get_package_share_directory
from ament_index_python import get_package_prefix
import glob
from robotic_msgs.action import RoboticTasks
from robotic_ai_model.rt1_jax import load_policy


class TaskClient(Node):

    def __init__(self):
        super().__init__('task_action_client')
        self._action_client = ActionClient(self, RoboticTasks, 'task_server')

    def send_goal(self, order):
        goal_msg = RoboticTasks.Goal()
        goal_msg.task_sequences = order

        self._action_client.wait_for_server()

        send_goal_future = self._action_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_goal_future)

        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return None

        get_result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, get_result_future)

    def get_last_file(directory_path):
        # Get all files in the directory
        files = glob.glob(os.path.join(directory_path, '*'))
        
        # Filter out directories
        files = [f for f in files if os.path.isfile(f)]
        
        # Sort files by modification time
        files.sort(key=os.path.getmtime)
        
        # Get the last file in the sorted list
        if files:
            last_file = files[-1]
            return last_file
        else:
            return None
        return get_result_future.result().result

def main(args=None):
    rclpy.init(args=args)
    action_client = TaskClient()
    command_input = input("Please enter the command in text: ")
    outputPack = get_package_share_directory("robotic_actions")
    outputDir = os.path.join(outputPack, "output")
    ## list files from output directory
    lastframe_path = TaskClient.get_last_file(outputDir)
    print(lastframe_path)
    image = np.tile(np.asarray(Image.open(lastframe_path)), (15,1,1,1))
    # print(image)
    actions_result = load_policy.main(inputText=command_input, obvers=lastframe_path)
    action_client.send_goal_async(actions_result)
    print(actions_result)
    # print(actions_result)
    action_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()