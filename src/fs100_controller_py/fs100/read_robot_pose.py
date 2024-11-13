import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import os
import sys

# Include the test module directory
test_dir = os.path.dirname(os.path.realpath(__file__))
module_dir = os.path.dirname(test_dir)
sys.path.append(module_dir)

from fs100_controller_py.fs100 import FS100
class RobotPosePublisher(Node):

    def __init__(self):
        super().__init__('robot_pose_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        robot_controller = FS100(ip="10.0.0.2")
        pos_info = self.get_robot_current_position(robot_controller)
        
        if pos_info is not None:
            msg = String()
            msg.data = str(pos_info)  # Convert pos_info to string to be published
            self.publisher_.publish(msg)
            self.get_logger().info(f'Position: "{msg.data}"')
        else:
            self.get_logger().error('Failed to retrieve robot position')
        
        self.i += 1

    def get_robot_current_position(self, fs100, robot_no=101):
        """
        Retrieve the current position of the robot.

        Args:
            fs100 (FS100): Instance of the FS100 class.
            robot_no (int, optional): Robot number. Defaults to 101.

        Returns:
            dict: A dictionary with position details if successful; otherwise, None.
        """
        pos_info = {}
        status = fs100.read_position(pos_info, robot_no=robot_no)

        if status == FS100.ERROR_SUCCESS:
            return pos_info
        else:
            print(f"Failed to retrieve robot position. Error code: {fs100.errno}")
            return None


def main(args=None):
    rclpy.init(args=args)

    robot_pose_publisher = RobotPosePublisher()

    rclpy.spin(robot_pose_publisher)

    # Destroy the node explicitly
    robot_pose_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
