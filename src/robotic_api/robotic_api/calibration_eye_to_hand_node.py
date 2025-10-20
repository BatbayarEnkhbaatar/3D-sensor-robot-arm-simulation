import rclpy
from rclpy.node import Node
import numpy as np
from robotic_msgs.msg import HoleDetectionResult as xyzrpy_msgs
from robotic_msgs.msg import YaskawaTasksGripper as gripper_msgs
from algorithms import calibration_eye_to_hand
from std_msgs.msg import Float64MultiArray
import time

class HandEyeCalib(Node):
    def __init__(self):
        super().__init__('hand_eye_calibration_node_sub_pub')

        self.subscription = self.create_subscription(
            Float64MultiArray, 
            '/detection_results',
            self.hole_detection_callback,  # Correct callback
            10
        )

        self.xyzrpy_publisher = self.create_publisher(xyzrpy_msgs, 'computed_xyzrpy', 10)
        self.gripper_publisher = self.create_publisher(gripper_msgs, 'gripper_command', 10)

        self.get_logger().info("Hand-Eye Calibration Node is ready! Listening for detection results...")

    def hole_detection_callback(self, msg):
        self.get_logger().info("Received holes.. now computing Hand-Eye calibration..")
        if not msg.data:
            self.get_logger().warn("Received empty hole detection coordinates.")
            return
        self.get_logger().info(f"Received detected coordinates: {msg.data}")
        self.compute_and_publish_xyzrpy(msg)

    def compute_and_publish_xyzrpy(self, target_point_msg):
        self.get_logger().info(f"Processing Sensor Coordinates: {target_point_msg.data}")
        
        target_point = np.array(target_point_msg.data, dtype=np.float64)
        target_point = np.append(target_point, 1.0).reshape(4, 1)

        end_effector_pose = np.array(calibration_eye_to_hand.get_tool_pose(target_point), dtype=np.float64).tolist()
        end_effector_pose = end_effector_pose[:-1]

        rpy = [-179.0698, -0.2457, 84.5689]
        end_effector_pose.extend(rpy)
        
        gripper_msg = gripper_msgs()
        self.get_logger().info(f"OPEN GRIPPER : {self.gripper_publisher}")
        gripper_msg.gripper_command = 1
        self.gripper_publisher.publish(gripper_msg)
        time.sleep(5)
        # Adjust position offsets
        end_effector_pose[0] += 15
        end_effector_pose[1]
        end_effector_pose[2] -= 15
        msg = xyzrpy_msgs()
        msg.xyzrpy = end_effector_pose
        self.xyzrpy_publisher.publish(msg)
        self.get_logger().info(f"Approaching to object , according to Hand-Eye Calibration : {msg.xyzrpy}")
        

        time.sleep(6)
        self.get_logger().info(f"GRASPING : {self.gripper_publisher}")
        gripper_msg.gripper_command = 2  # Close gripper
        self.gripper_publisher.publish(gripper_msg)



        # time.sleep(8)
        # msg.xyzrpy = end_ef_pose1
        # self.xyzrpy_publisher.publish(msg)
        # self.get_logger().info(f"Lifting up: {msg.xyzrpy}")
        # time.sleep(4)


        # throwing away
        time.sleep(5)
        end_ef_pose2 = [538.620, 259.033, 370.305, -170.1313, -8.0149, -70.8824]
        msg = xyzrpy_msgs()
        msg.xyzrpy = end_ef_pose2
        self.xyzrpy_publisher.publish(msg)
        self.get_logger().info(f"Throwing away Pose: {msg.xyzrpy}")
        time.sleep(6)
        gripper_msg = gripper_msgs()
        self.get_logger().info(f"Gripper Command to OPEN to loose : {self.gripper_publisher}")
        gripper_msg.gripper_command = 1  # Open gripper
        self.gripper_publisher.publish(gripper_msg)

        time.sleep(4)
        # Move to initial pose
        # msg.xyzrpy = [374.2910, -42.9830, 358.247, -170.1321, -8.0119, -70.8800]
        msg.xyzrpy  = [527.642, -67.951, 324.796, -179.0715, -0.2486, 84.5657]
        self.get_logger().info("End-effector goes back to Initial pose within a sec...")
        self.xyzrpy_publisher.publish(msg)
        time.sleep(6)
        self.get_logger().info(f"Gripper Command to CLOSE : {self.gripper_publisher}")
        gripper_msg.gripper_command = 2  # Close gripper
        self.gripper_publisher.publish(gripper_msg)

def main(args=None):
    rclpy.init(args=args)
    node = HandEyeCalib()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
