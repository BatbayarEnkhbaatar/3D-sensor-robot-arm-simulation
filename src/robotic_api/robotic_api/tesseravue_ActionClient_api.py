import rclpy
from rclpy.node import Node
import numpy as np
from std_msgs.msg import Float64MultiArray
from robotic_msgs.msg import HoleDetectionResult as xyzrpy_msgs
from algorithms import calibration_eye_to_hand
from robotic_msgs.msg import YaskawaTasksGripper as gripper_msgs
import time
import threading
from flask import Flask, request, jsonify

# ROS2 Node
class HandEyeCalib(Node):
    def __init__(self):
        super().__init__('hand_eye_calibration_node_sub_pub')
        # self.publisher = self.create_publisher(xyzrpy_msgs, 'computed_xyzrpy', 10)
        self.xyzrpy_publisher = self.create_publisher(xyzrpy_msgs, 'computed_xyzrpy', 10)
        self.gripper_publisher = self.create_publisher(gripper_msgs, 'gripper_command', 10)
        self.get_logger().info("Hand-Eye Calibration Node is ready!")

    def compute_and_publish_xyzrpy_from_array(self, point_array):
        """Wraps point as Float64MultiArray and processes."""
        msg = Float64MultiArray()
        msg.data = point_array
        self.compute_and_publish_xyzrpy(msg)

    def compute_and_publish_xyzrpy(self, target_point_msg):
        self.get_logger().info(f"Processing Sensor Coordinates: {target_point_msg.data}")
        
        target_point = np.array(target_point_msg.data, dtype=np.float64)
        target_point = np.append(target_point[:3], 1.0).reshape(4, 1)

        end_effector_pose = np.array(calibration_eye_to_hand.get_tool_pose(target_point), dtype=np.float64).tolist()
        end_effector_pose = end_effector_pose[:-1]
        # rpy = [-179.0698, -0.2457, 84.5689]
        rpy = [-179.0703, -0.2495, 86.4242]
        end_effector_pose.extend(rpy)
        
        gripper_msg = gripper_msgs()
        self.get_logger().info(f"OPEN GRIPPER : {self.gripper_publisher}")
        gripper_msg.gripper_command = 1  # Open gripper
        self.gripper_publisher.publish(gripper_msg)

        time.sleep(3)
        # Adjust position offsets
        end_effector_pose[0]
        end_effector_pose[1]
        end_effector_pose[2] += 50
        msg = xyzrpy_msgs()
        msg.xyzrpy = end_effector_pose
        self.xyzrpy_publisher.publish(msg)
        self.get_logger().info(f"1st Stop , according to Hand-Eye Calibration : {msg.xyzrpy}")
        
        time.sleep(6)
        # Adjust position offsets
        end_effector_pose[0] 
        end_effector_pose[1]
        end_effector_pose[2] -= 58
        msg = xyzrpy_msgs()
        msg.xyzrpy = end_effector_pose
        self.xyzrpy_publisher.publish(msg)
        self.get_logger().info(f"Approaching to object , according to Hand-Eye Calibration : {msg.xyzrpy}")
        


        time.sleep(3)
        self.get_logger().info(f"GRASPING : {self.gripper_publisher}")
        gripper_msg.gripper_command = 2  # Close gripper
        self.gripper_publisher.publish(gripper_msg)
        time.sleep(4)
        # Adjust position offsets
        end_effector_pose[0]
        end_effector_pose[1]
        end_effector_pose[2] += 50
        msg = xyzrpy_msgs()
        msg.xyzrpy = end_effector_pose
        self.xyzrpy_publisher.publish(msg)
        self.get_logger().info(f"3st Stop , according to Hand-Eye Calibration : {msg.xyzrpy}")
        # throwing away
        time.sleep(3)
        end_ef_pose2 = [538.620, 259.033, 370.305, -170.1313, -8.0149, -70.8824]
        msg = xyzrpy_msgs()
        msg.xyzrpy = end_ef_pose2
        self.xyzrpy_publisher.publish(msg)
        self.get_logger().info(f"Throwing away Pose: {msg.xyzrpy}")

        time.sleep(4)
        end_ef_pose2 = [617.237, 175.858, -161.825, -170.1313, -8.0149, -70.8824]
        msg = xyzrpy_msgs()
        msg.xyzrpy = end_ef_pose2
        self.xyzrpy_publisher.publish(msg)
        self.get_logger().info(f"Dropping the object: {msg.xyzrpy}")
        time.sleep(4)
        gripper_msg = gripper_msgs()
        self.get_logger().info(f"Gripper Command to OPEN to loose : {self.gripper_publisher}")
        gripper_msg.gripper_command = 1  # Open gripper
        self.gripper_publisher.publish(gripper_msg)
        time.sleep(3)
        # Move to initial pose

        # msg.xyzrpy  = [527.642, -67.951, 324.796, -179.0715, -0.2486, 84.5657]  #original pose


        #drop [617.237, 175.858, -161.825 -179.0703, -0.2495, 86.4242]
        msg.xyzrpy = [527.646, -67.943, 324.786, -179.0703, -0.2495, 86.4242]
        self.get_logger().info("End-effector goes back to Initial pose within a sec...")
        self.xyzrpy_publisher.publish(msg)
        time.sleep(7)
        self.get_logger().info(f"Gripper Command to CLOSE : {self.gripper_publisher}")
        gripper_msg.gripper_command = 2  # Close gripper
        self.gripper_publisher.publish(gripper_msg)


# Flask Server
app = Flask(__name__)
ros_node = None

@app.route('/targetpoint', methods=['POST'])
def handle_target_points():
    data = request.get_json()
    if not data or 'target_point' not in data:
        return jsonify({'error': 'Missing "target_point" field'}), 400

    points_list = data['target_point']

    print("target_point field TYPE:", type(points_list))  # <--- current print
    # for points in points_list:
    #     if not isinstance(points, list) or not all(isinstance(p, list) and len(p) == 3 for p in points):
    #         return jsonify({'error': '"target_point" must be a list of [x, y, z]'}), 400

    interval = data.get('interval', 5)  # default to 5 seconds between points

    def process_points():
        for pt in points_list:
            ros_node.get_logger().info(f"Processing target point: {pt}")
            ros_node.compute_and_publish_xyzrpy_from_array(pt)
            time.sleep(interval)

    # Run in a thread to avoid blocking Flask
    threading.Thread(target=process_points, daemon=True).start()

    return jsonify({'status': f'Processing {len(points_list)} target points with {interval}s interval'}), 200


def start_flask():
    app.run(host='0.0.0.0', port=5010)


def main(args=None):
    global ros_node
    rclpy.init(args=args)
    ros_node = HandEyeCalib()

    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    rclpy.spin(ros_node)
    ros_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
