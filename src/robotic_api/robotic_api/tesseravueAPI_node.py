import os
import threading
import io
import numpy as np
from PIL import Image
from flask import Flask, jsonify, send_from_directory
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from ament_index_python.packages import get_package_share_directory

from robotic_msgs.action import TesseraVueTasks
from tesseravue.tesseravue_client import BinpickingClient
from tesseravue.binpicking_processor import ObjectDetector3D
from std_srvs.srv import Trigger

app = Flask(__name__)
ros_node = None  # Global ROS node reference
_last_capture = None  # Cached capture data
detector = None  # Global detector

class TesseraVueClientNode(Node):
    SENSOR_IP = "192.168.0.10"
    SENSOR_PORT = 1024
    # MODEL_PATH = "model_19.pt"
    # CAD_MODEL_PATH = "SCREW2.pcd"

    def __init__(self):


        super().__init__('tesseraVue_client_node')

        self._action_client = ActionClient(self, TesseraVueTasks, "TesseraVueTasks")
        self.get_logger().info("TesseraVue Client Node is Ready...")

        package_name = 'robotic_3dsensor'
        self.package_share_directory = get_package_share_directory(package_name)
        self.local_directory = os.path.join(self.package_share_directory, 'data/')
        self.local_model = os.path.join(self.package_share_directory, 'model/')
        self.MODEL_PATH = self.local_model + "model_19.pt"
        self.CAD_MODEL_PATH = self.local_model + "SCREW2.pcd"
        os.makedirs(self.local_directory, exist_ok=True)

        self.last_img = None
        self.last_pcd = None

    def get_data(self):
        try:
            with BinpickingClient(self.SENSOR_IP, self.SENSOR_PORT, root_dir=self.local_directory) as cli:
                img, pcd = cli.capture(save_png=True, save_pcd=True)

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


    def call_trigger_service(self):
        client = self.create_client(Trigger, '/trigger_data_capture')
        if not client.wait_for_service(timeout_sec=3.0):
            self.get_logger().error("Service /trigger_data_capture not available.")
            return False, "Service not available"

        request = Trigger.Request()
        future = client.call_async(request)

        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            result = future.result()
            return result.success, result.message
        else:
            self.get_logger().error("Service call failed")
            return False, "Service call failed"


@app.route("/capture", methods=["GET"])
def capture():
    global _last_capture

    if not ros_node:
        return jsonify({"error": "ROS Node not initialized"}), 500

    try:
        with BinpickingClient(
            TesseraVueClientNode.SENSOR_IP,
            TesseraVueClientNode.SENSOR_PORT,
            root_dir=ros_node.local_directory
        ) as cli:
            raw_img, (X, Y, Z, depth), (ch, w, h), prefix = cli.capture(
                channel=0,
                save_png=True,
                save_pcd=True
            )

        img = Image.frombytes("L", (w, h), raw_img)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png_bytes = buf.getvalue()

        xyz = np.dstack([
            np.array(X).reshape((h, w)),
            np.array(Y).reshape((h, w)),
            np.array(Z).reshape((h, w))
        ])

        _last_capture = {
            "png_bytes": png_bytes,
            "xyz": xyz,
            "channels": ch,
            "width": w,
            "height": h,
            "pointcloud": {"X": X, "Y": Y, "Z": Z, "depth": depth}
        }

        return jsonify({"prefix": prefix})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/detect", methods=["GET"])
def detect():
    if not _last_capture:
        return jsonify({"error": "No capture in memory. Call /capture first."}), 400

    try:
        png_bytes = _last_capture["png_bytes"]
        xyz = _last_capture["xyz"]

        result = detector.process(png_bytes, xyz)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

@app.route('/trigger', methods=['GET'])
def trigger_capture():
    if ros_node:
        success, message = ros_node.call_trigger_service()
        return jsonify({"success": success, "message": message})
    else:
        return jsonify({"success": False, "message": "ROS Node not ready"}), 500

@app.route('/send', methods=['POST'])
def trigger_capture():
    if ros_node:
        success, message = ros_node.call_trigger_service()
        return jsonify({"success": success, "message": message})
    else:
        return jsonify({"success": False, "message": "ROS Node not ready"}), 500


def ros_spin():
    while rclpy.ok():
        rclpy.spin_once(ros_node, timeout_sec=0.1)


def main():
    global ros_node, detector

    rclpy.init()
    ros_node = TesseraVueClientNode()
    detector = ObjectDetector3D(
        ros_node.MODEL_PATH,
        ros_node.CAD_MODEL_PATH
    )

    ros_thread = threading.Thread(target=ros_spin, daemon=True)
    ros_thread.start()

    app.run(port=5000, host='0.0.0.0')


if __name__ == '__main__':
    main()
