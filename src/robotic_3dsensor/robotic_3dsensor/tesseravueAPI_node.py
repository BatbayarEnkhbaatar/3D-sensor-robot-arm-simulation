import os
import threading
from flask import Flask, jsonify, send_from_directory
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from ament_index_python.packages import get_package_share_directory
from robotic_msgs.action import TesseraVueTasks
from tesseravue import tesseravue_client

app = Flask(__name__)
ros_node = None  # Global reference to the ROS node


class TesseraVueClientNode(Node):
    def __init__(self): 
        super().__init__('tesseraVue_client_node')
        self._action_client = ActionClient(self, TesseraVueTasks, "TesseraVueTasks")
        self.get_logger().info("TesseraVue Client Node is Ready...")

        package_name = 'robotic_3dsensor'
        self.package_share_directory = get_package_share_directory(package_name)
        self.local_directory = os.path.join(self.package_share_directory, 'data/')
        os.makedirs(self.local_directory, exist_ok=True)

        # Store last filenames for download access
        self.last_img = None
        self.last_pcd = None

    def get_data(self):
        try:
            sensor_ip = "192.168.0.10"
            sensor_port = 1024
            img, pcd = tesseravue_client._cli(ip=sensor_ip, tcp=sensor_port, strPath=self.local_directory)
            self.get_logger().info(f"Image saved: {img}")
            self.get_logger().info(f"Point Cloud saved: {pcd}")

            self.last_img = img
            self.last_pcd = pcd

            self._send_action_goal([pcd, img])
            
            return True, f"pcd: {self.last_pcd}, img: {self.last_img}"
        except Exception as er:
            self.get_logger().error(f"Error capturing data: {str(er)}")
            return False, str(er)

    def _send_action_goal(self, goal):
        self.get_logger().info("Sending goal to the action server...")
        goal_msg = TesseraVueTasks.Goal()
        goal_msg.lastshots = goal
        send_goal_future = self._action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().info('File Transaction rejected :(')
                return
            self.get_logger().info('File Transaction accepted :)')
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(self.get_result_callback)
        except Exception as e:
            self.get_logger().error(f"Goal response callback failed: {str(e)}")

    def get_result_callback(self, future):
        try:
            result = future.result().result
            self.get_logger().info(f'File Transaction: {result.ftpsuccess}')
        except Exception as e:
            self.get_logger().error(f"Result callback failed: {str(e)}")


@app.route('/takeshots', methods=['GET'])
def take_shots():
    if ros_node:
        success, message = ros_node.get_data()
        return jsonify({"success": success, "message": message})
    else:
        return jsonify({"success": False, "message": "ROS Node not ready"}), 500


@app.route('/download/pcd/<filename>', methods=['GET'])
def download_pcd(filename):
    if ros_node:
        return send_from_directory(ros_node.local_directory, filename, as_attachment=True)
    else:
        return jsonify({"success": False, "message": "ROS Node not ready"}), 500


@app.route('/download/img/<filename>', methods=['GET'])
def download_img(filename):
    if ros_node:
        return send_from_directory(ros_node.local_directory, filename, as_attachment=True)
    else:
        return jsonify({"success": False, "message": "ROS Node not ready"}), 500


def ros_spin():
    while rclpy.ok():
        rclpy.spin_once(ros_node, timeout_sec=0.1)


def main():
    global ros_node
    rclpy.init()
    ros_node = TesseraVueClientNode()

    # Start ROS spinning in a separate thread
    ros_thread = threading.Thread(target=ros_spin, daemon=True)
    ros_thread.start()

    # Start Flask app (can also specify host='0.0.0.0' for external access)
    app.run(port=5000)


if __name__ == '__main__':
    main()
