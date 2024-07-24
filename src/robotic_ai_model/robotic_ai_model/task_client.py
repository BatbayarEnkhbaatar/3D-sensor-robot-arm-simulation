#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import os
import glob
from rclpy.action.client import ClientGoalHandle
from ament_index_python.packages import get_package_share_directory
from robotic_msgs.action import RoboticTasks
from robotic_ai_model.rt1_jax import load_policy

class TaskClient(Node):
    # Loading the model checkpoints for the model in the ROS2 node spinning
    policy_loaded, embed = load_policy.load_check_points()

    def __init__(self):
        super().__init__('RoboticTaskClient_Node')
        self._action_client = ActionClient(self, RoboticTasks, 'task_server')
        self._action_client.wait_for_server()
        self.get_logger().info('Action server ready.')

    def send_goal(self):
        # Creating goal
        goal_msg = RoboticTasks.Goal()
        command_input = input("Please enter the command in text: ")
        output_pack = get_package_share_directory("robotic_actions")
        output_dir = os.path.join(output_pack, "output")
        last_frame_path = get_last_file(output_dir)
        self.get_logger().info("Camera Last Frame: " + str(last_frame_path))
        
        if last_frame_path:
            try:
                order = load_policy.main(policy=self.policy_loaded, embed=self.embed, obvers=last_frame_path, inputText=command_input)
                ac_seq = [float(i) for i in order]
                goal_msg.task_sequences = ac_seq
            except Exception as e:
                self.get_logger().error(f"Error in generating action sequences: {e}")
                return
        else:
            self.get_logger().error("No frame found in the output directory.")
            return

        # Sending a goal to Task Server through the ROS2 interface
        self.get_logger().info("Sending the goal...")
        send_goal_future = self._action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().info("Goal rejected :(")
                return

            self.get_logger().info("Goal accepted :)")
            get_result_future = goal_handle.get_result_async()
            get_result_future.add_done_callback(self.goal_result_callback)
        except Exception as e:
            self.get_logger().error(f"Error in goal response callback: {e}")

    def goal_result_callback(self, future):
        try:
            result = future.result().result
            self.get_logger().info("Result: " + str(result.success))
            self.send_goal()  # Prompt for the next goal
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
    node_client.send_goal()
    rclpy.spin(node_client)
    node_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
