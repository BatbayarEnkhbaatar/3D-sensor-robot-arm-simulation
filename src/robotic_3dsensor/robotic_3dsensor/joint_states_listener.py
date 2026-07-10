import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np

class JointStateListener(Node):
    def __init__(self):
        super().__init__('joint_state_listener')
        
        # Subscribe to the /joint_states topic
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10  # Queue size
        )
        
        # Timer to print joint states every 1 second
        self.timer = self.create_timer(1.0, self.timer_callback)  # 1 Hz
        self.latest_joint_names = []
        self.latest_joint_positions = np.array([])

        self.get_logger().info("Subscribed to /joint_states and printing every 1s.")

    def joint_state_callback(self, msg):
        """ Store latest joint states received from topic. """
        self.latest_joint_names = msg.name
        self.latest_joint_positions = np.degrees(msg.position)  # Convert to degrees

    def timer_callback(self):
        """ Print latest joint states every 1 second. """
        if len(self.latest_joint_names) == 0 or len(self.latest_joint_positions) == 0:
            self.get_logger().warn("No joint data received yet!")
            return
        lists_joint_ankles = []
        self.get_logger().info("Joint Angles (Degrees):")
        for name, deg in zip(self.latest_joint_names, self.latest_joint_positions):
            self.get_logger().info(f"{name}: {deg:.2f}°")
            lists_joint_ankles.append(deg)
        self.get_logger().info(f"Joint Angles (Degrees): {str(lists_joint_ankles)}")

def main(args=None):
    rclpy.init(args=args)
    node = JointStateListener()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
