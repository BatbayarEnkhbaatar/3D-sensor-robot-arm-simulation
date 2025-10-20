import rclpy
from rclpy.node import Node
from robotic_msgs.msg import YaskawaTasksGripper as gripper_msg

import os
import sys
import threading

# Add module path for fs100_controller_py
# script_dir = os.path.dirname(os.path.realpath(__file__))
# module_dir = os.path.dirname(script_dir)
# sys.path.append(module_dir)
from fs100_controller_py.fs100 import FS100
import fs100_gripper_controller.control_gripper_jbi  as grip_command


class FS100Subscriber(Node):
    def __init__(self):
        super().__init__('fs100_gripper_subscriber')
        # Initialize FS100 Controller
        self.robot_controller = FS100(ip="10.0.0.2")
        # Create subscriber to "gripper_command"

        self.subscription = self.create_subscription(
            gripper_msg,
            'gripper_command',
            self.execute_motion,
            10
        )

        self.get_logger().info("FS100 Subscriber node for GRipper Controller gets started.")

    def execute_motion(self, msg):
        command = msg.gripper_command
        # Transform the coordinates to FS100 format
        self.get_logger().info(f"Gripper Command: {str(command)}")
        if command == 1:
            self.get_logger().info(f"Gripper is openning")
        elif command ==2:
            self.get_logger().info(f"Gripper is clossing")

        grip_comm_result =  grip_command.gripper_comma(ROBOT_IP="10.0.0.2", 
                                                COMMAND=command)

        if grip_comm_result =="success":
            self.get_logger().info("FS100 command executed successfully.")
        else:
            self.get_logger().error(f"Failed to move robot. Error code: {self.robot_controller.errno}")
        

def main(args=None):
    rclpy.init(args=args)
    node = FS100Subscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
