#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import os
from PIL import Image
import numpy as np
from rclpy.action.client import ClientGoalHandle
from ament_index_python.packages import get_package_share_directory
import glob
from robotic_msgs.action import RoboticTasks
from robotic_ai_model.rt1_jax import load_policy

class TaskClient(Node):
    # loading the model check points for the model in the ROS2 node spinning and which means getting ready to quickly perform the next tasks comming from ...
    policy_loaded, embed = load_policy.load_check_points()

    def __init__(self):
        super().__init__('RoboticTaskClient_Node')
        self._action_client = ActionClient(self, RoboticTasks, 'task_server')
        
    def send_goal(self):
        self._action_client.wait_for_server()

        # Creating goal
        goal_msg = RoboticTasks.Goal()
        

        result = True
        while result:
            command_input = input("Please enter the command in text: ")
            output_pack = get_package_share_directory("robotic_actions")
            output_dir = os.path.join(output_pack, "output")
            last_frame_path = get_last_file(output_dir)
            self.get_logger().info("Camera Last Frame: " + last_frame_path)
            order = load_policy.main(policy=self.policy_loaded, embed=self.embed, obvers=last_frame_path, inputText=command_input)
            ac_seq = [float(i) for i in order]
            goal_msg.task_sequences = ac_seq

            # Sending a goal to Task Server through the ROS2 interface
            self.get_logger().info("Sending the goal...")
            self._action_client.send_goal_async(goal_msg).add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self.goal_handle_: ClientGoalHandle = future.result()
        if self.goal_handle_.accepted:
            self.goal_handle_.get_result_async().add_done_callback(self.goal_result_callback)
        return 0

    def goal_result_callback(self, future):
        result = future.result().result
        self.get_logger().info("Result: " + str(result.success))
        self.send_goal()
        return 0

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

def main(args=None):
    rclpy.init(args=args)
    node_client = TaskClient()
    node_client.send_goal()
    rclpy.spin(node_client)
    node_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
