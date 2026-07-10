import rclpy
from rclpy.node import Node
import numpy as np
from robotic_msgs.msg import HoleDetectionResult  as xyzrpy_msgs
from algorithms import calibration_eye_to_hand2_top2down
from std_msgs.msg import Float64MultiArray
import time
class HandEyeCalib(Node):
    def __init__(self):
        super().__init__('hand_eye_calibration_node_sub_pub')

        # Subscriber to receive hole detection results
        self.subscription = self.create_subscription(
            Float64MultiArray,  # Replace with actual message type
            '/detection_results',
            self.compute_and_publish_xyzrpy,
            10
        )

        # Publisher for computed XYZRPY
        self.publisher = self.create_publisher(xyzrpy_msgs, 'computed_xyzrpy', 10)

        self.get_logger().info("Hand-Eye Calibration Node is ready! Listening for hole detection results... on topic detection_results ")

    def hole_detection_callback(self, msg):
        """
        Extracts hole detection results,
        computes the transformed XYZRPY, and publishes the result.
        """
        self.get_logger().info(f"Received holes.. now computing Hand-Eye calibration..  ")
        objects_xyz = msg.data  # Adjust based on actual message field

        if not objects_xyz:
            self.get_logger().warn("Received empty hole detection coordinates.")
            return
        self.get_logger().info(f"Received detected coordinates: {objects_xyz}")
        self.compute_and_publish_xyzrpy(objects_xyz)

    def compute_and_publish_xyzrpy(self, target_point):
        """Processes object coordinates using Hand-Eye Calibration and publishes."""
        self.get_logger().info(f"Processing Sensor Coordinates: {target_point}")
        # target_point.data = [87.91, -7.10, 663.91]
        # Convert to homogeneous coordinates         
        target_point = np.array(target_point.data, dtype=np.float64)   
        target_point = np.append(target_point, 1.0).reshape(4, 1)                            
     
        end_effector_pose = (np.array(calibration_eye_to_hand2_top2down.get_tool_pose(target_point), dtype=np.float64) / 1000).tolist()
        self.get_logger().info(f"Hand-Eye Calibration Result0: {end_effector_pose}")
        end_effector_pose = end_effector_pose[:-1] 
        rpy = [2.439, 1.063 ,-2.596]
        for element in rpy:
            end_effector_pose.append(element)

        msg = xyzrpy_msgs()
        msg.xyzrpy = end_effector_pose
        self.publisher.publish(msg)
        self.get_logger().info(f"Hand-Eye Calibration Result: {end_effector_pose}")
        
        # going back to home pose
        time.sleep(15)
        msg.xyzrpy = [-0.33569, -0.13998, 0.61284, 2.832, 2.856, -2.203] # LOWER POSE 
        msg.xyzrpy =  [0.02578, 0.31763, 0.69148, 2.5, 1.388, -2.621] # Top to Down position 
        self.get_logger().info(f"End-effector goes back to Iniital pose within 10 sec...")        
        self.publisher.publish(msg)
        time.sleep(8)
        
        ####################################
        ####################################
        ####################################

        # msg.xyzrpy = [-0.13306, 0.05625, 0.41891, 3.867, 1.684, 1.245]
        
def main(args=None):
    rclpy.init(args=args)
    node = HandEyeCalib()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
