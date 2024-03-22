import rclpy
from std_msgs.msg import Float64MultiArray
from rclpy.node import Node

class GripperControllerPublisher(Node):
    def __init__(self):
        super().__init__('gripper_controller_publisher')
        self.publisher_ = self.create_publisher(Float64MultiArray, '/gripper_controller/commands', 10)
        self.timer = self.create_timer(0.5, self.publish_message)
        self.msg = Float64MultiArray()

    def publish_message(self):
        # Prompt the user for input
        gripper_cmd = float(input("Enter the gripper command (open or close): "))
        # gripper_o_degree = float(input("Enter the openning degree of the gripper"))
        # Create the message
        self.msg.layout.dim = []
        self.msg.layout.data_offset = 0
        self.msg.data = [gripper_cmd]  # Set the gripper command value as a list containing the user input converted to float

        # Publish the message
        self.publisher_.publish(self.msg)
        self.get_logger().info('Published: %s' % self.msg.data)

def main(args=None):
    rclpy.init(args=args)
    gripper_controller_publisher = GripperControllerPublisher()
    rclpy.spin(gripper_controller_publisher)
    gripper_controller_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
