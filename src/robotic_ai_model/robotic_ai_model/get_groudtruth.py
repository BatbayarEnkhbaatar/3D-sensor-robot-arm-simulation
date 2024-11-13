import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf2_ros import TransformListener, Buffer
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException

class PoseListener(Node):
    def __init__(self):
        super().__init__('pose_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.target_frame = 'base_link'
        self.source_frame = 'link_t'
        self.get_logger().info("IK getting is started")

    def get_pose(self):
        try:
            # Get the transform from source_frame to target_frame
            trans = self.tf_buffer.lookup_transform(self.target_frame, self.source_frame, rclpy.time.Time())
            pose_stamped = PoseStamped()
            pose_stamped.header = trans.header
            pose_stamped.pose.position.x = trans.transform.translation.x
            pose_stamped.pose.position.y = trans.transform.translation.y
            pose_stamped.pose.position.z = trans.transform.translation.z
            pose_stamped.pose.orientation = trans.transform.rotation

            return pose_stamped
        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().error(f"Could not transform {self.target_frame} to {self.source_frame}: {e}")
            return None

def main(args=None):
    rclpy.init(args=args)
    node = PoseListener()
    rclpy.spin_once(node)

    pose_stamped = node.get_pose()
    if pose_stamped:
        node.get_logger().info(f"Pose: {pose_stamped}")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
