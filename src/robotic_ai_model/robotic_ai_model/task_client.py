#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import os
import glob
from ament_index_python.packages import get_package_share_directory
from robotic_msgs.action import RoboticTasks
import requests
import re

class TaskClient(Node):

    url = 'http://127.0.0.1:5000/command'

    def __init__(self):
        super().__init__('RoboticTaskClient_Node')
        self._action_client = ActionClient(self, RoboticTasks, 'task_server')
        self._action_client.wait_for_server()
        self.get_logger().info('Action Client ready.')
        self.new_goal = True
        self.terminate_epi = [0, 1, 0]
        self.response_data = ""
    
    def send_goal(self):
        # Creating goal
        goal_msg = RoboticTasks.Goal()

        command_input = input("Please enter the command in text: ")
        

        while self.terminate_epi != [1, 0, 0]: 
            
            output_pack = get_package_share_directory("robotic_actions")
            output_dir = os.path.join(output_pack, "output")
            last_frame_path = get_last_file(output_dir)
            self.get_logger().info("Camera Last Frame: " + str(last_frame_path))
            if last_frame_path:
                with open(last_frame_path, 'rb') as file:
                    files = {'image': file}
                    data = {'text': command_input}
                    response = requests.post(self.url, files=files, data=data)
                    response.raise_for_status()  
                    self.response_data = response.json()
                    self.get_logger().info(f"RT-1 generated : {self.response_data}")
                    response_data_action = self.response_data[0]
                if 'action_six_dim' in response_data_action:
                    order_str = response_data_action['action_six_dim']
                    order = re.findall(r"[-+]?\d*\.\d+|\d+", order_str)
                    ac_seq = [float(i) for i in order]
                    goal_msg.task_sequences = ac_seq

            else:
                self.get_logger().error("No frame found in the output directory.")
        
            self.get_logger().info("Sending the goal...")
            send_goal_future = self._action_client.send_goal_async(goal_msg)
            send_goal_future.add_done_callback(self.goal_response_callback)


            response_data_termination = self.response_data[2]
            if 'ter_ep_val' in response_data_termination:
                self.terminate_epi = response_data_termination['ter_ep_val']
            else:
                self.get_logger().error("Termination Episode is not found") 
        
        response_data_gripper = self.response_data[1]

        if 'gripper_action' in response_data_gripper:
            gripper_action = response_data_gripper['gripper_action']
            goal_msg.task_gripper = gripper_action
        else:
            self.get_logger().error("Gripper action is not found")

    def goal_response_callback(self, future):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().info("Goal rejected :(")
            else:
                self.get_logger().info("Goal accepted :)")
                get_result_future = goal_handle.get_result_async()
                get_result_future.add_done_callback(self.goal_result_callback)
        except Exception as e:
            self.get_logger().error(f"Error in goal response callback: {e}")
        
    
    def goal_result_callback(self, future):
        try:
            result = future.result().result
            self.get_logger().info("Result: " + str(result.success))
            self.get_logger().info("Terminate Episode: " + str(result.terminate_episode))
            self.new_goal = True
        except Exception as e:
            self.get_logger().error(f"Exception in result callback: {e}")

def get_last_file(directory_path):
    try:
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
    except Exception as e:
        print(f"Error in getting last file: {e}")
        return None

def main(args=None):
    rclpy.init(args=args)
    node_client = TaskClient()
    # rclpy.spin(node_client)
    while node_client.new_goal:
        node_client.send_goal()
        rclpy.spin_once(node_client, timeout_sec=0.5)
    node_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
