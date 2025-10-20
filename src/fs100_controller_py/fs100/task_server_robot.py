import rclpy
from rclpy.node import Node
from robotic_msgs.msg import HoleDetectionResult

import os
import sys
import threading

# Add module path for fs100_controller_py
script_dir = os.path.dirname(os.path.realpath(__file__))
module_dir = os.path.dirname(script_dir)
sys.path.append(module_dir)
from fs100_controller_py.fs100 import FS100
from fs100_gripper_controller import  gripper_control_dem


class FS100Subscriber(Node):
    def __init__(self):
        super().__init__('fs100_subscriber')
        # Initialize FS100 Controller
        self.robot_controller = FS100(ip="10.0.0.2")
        # Create subscriber to "computed_xyzrpy"

        self.subscription = self.create_subscription(
            HoleDetectionResult,
            'computed_xyzrpy',
            self.handle_detection_result,
            10
        )
        self.get_logger().info("FS100 Subscriber node for Robot Controller gets started.")

    def handle_detection_result(self, msg):
        if not msg.xyzrpy or len(msg.xyzrpy) < 6:
            self.get_logger().warn("Received invalid or empty xyzrpy data!")
            return

        self.get_logger().info(f"Received XYZRPY: {msg.xyzrpy}")
        threading.Thread(target=self.execute_motion, args=(msg.xyzrpy,)).start()

    def execute_motion(self, xyzrpy):
        # Transform the coordinates to FS100 format
        transformed_goal = [
            int(xyzrpy[0] * 1000),
            int(xyzrpy[1] * 1000),
            int(xyzrpy[2] * 1000),
            int(xyzrpy[3] * 10000),
            int(xyzrpy[4] * 10000),
            int(xyzrpy[5] * 10000)
        ]
        transformed_goal.extend([0, 0]) 
        # self.get_logger.info(f"RECIEVED XYZRPY : {str(xyzrpy)}")

        self.get_logger().info(f"Transformed FS100 Position: {transformed_goal}")

        result = self.robot_controller.mov(
            move_type=FS100.MOVE_TYPE_LINEAR_ABSOLUTE_POS,
            coordinate=FS100.MOVE_COORDINATE_SYSTEM_BASE,
            speed_class=FS100.MOVE_SPEED_CLASS_MILLIMETER,
            speed=3000,
            pos=transformed_goal        )

        if result == FS100.ERROR_SUCCESS:
            self.get_logger().info("FS100 command executed successfully.")
        else:
            self.get_logger().error(f"Failed to move FS100 robot. Error code: {self.robot_controller.errno}")
        

def main(args=None):
    rclpy.init(args=args)
    node = FS100Subscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
