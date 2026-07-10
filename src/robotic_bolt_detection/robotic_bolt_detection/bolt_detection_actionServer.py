import rclpy
import requests
from rclpy.node import Node
from rclpy.action import ActionServer
from robotic_msgs.action import TesseraVueTasks
import time
import json
import re
from std_msgs.msg import Header
from geometry_msgs.msg import Point
from robotic_msgs.msg import BoltDetectionResult
from std_msgs.msg import Float64MultiArray
import array
import time

class BoltDetectionNode(Node):
    def __init__(self):
        super().__init__('bolt_detection_Action_Server')
        self.publisher_ = self.create_publisher(Float64MultiArray, 'detection_results', 10)
        self.timer = self.create_timer(1.0, self.publish_bolt_detection_result)
        self.latest_result = None  # Store latest result

        # Initialize Action Server
        self._action_server = ActionServer(
            self,
            TesseraVueTasks,
            'TesseraVueTasks',
            self.execute_callback
        )
        self.get_logger().info("Bolt Detection Action Server started ...")

    def execute_callback(self, goal_handle):
        """Handles action goals by sending a POST request to the Docker container."""
        self.get_logger().info("Received request to process PCD and BMP files.")

        result = TesseraVueTasks.Result()
        feedback_msgs = TesseraVueTasks.Feedback()
        goal = goal_handle.request
        if goal.lastshots and len(goal.lastshots) >= 2:
            pcd_file = goal.lastshots[0]
            bmp_file = goal.lastshots[1]

        self.get_logger().info(f"PCD File: {pcd_file}")
        self.get_logger().info(f"Image File: {bmp_file}")


        # Set fixed file paths (for debugging)
        # pcd_file = "/home/ubuntu/Documents/my_work_1/ur_robot_driver/install/robotic_3dsensor/share/robotic_3dsensor/data/PRJ_[20250311_073743].pcd"
        # bmp_file = "/home/ubuntu/Documents/my_work_1/ur_robot_driver/install/robotic_3dsensor/share/robotic_3dsensor/data/CAM_[20250311_073745].bmp"
        
        # self.get_logger().info(f"Processing files: {pcd_file}, {bmp_file}")

        success, result_json = self.send_post_request(pcd_file, bmp_file)
        
        if success:
            self.latest_result = result_json  
            goal_handle.succeed()
            result.success = True
            # result.feedback = "Processing completed successfully."
        else:
            goal_handle.abort()
            result.success = False
            # result.feedback = "Processing failed."

        return result

    def extract_center_points(self, result_json):
        """Extracts bolt center points from the result JSON."""
        match = re.search(r"\{.*\}", str(result_json), re.DOTALL)
        if match:
            json_str = match.group(0)
        else:
            self.get_logger().error("No JSON found in the text.")
            return []

        try:
            data = json.loads(json_str)

            # Create a list to store center points.
            # We allocate a list with the same length as the number of objects.
            center_points = [None] * len(data["objects"])

            # Iterate over each object to extract its center_point values.
            for obj in data["objects"]:
                # Adjust the index since Python lists start at 0 (id 1 goes to index 0)
                index = obj["id"] - 1
                cp = obj["center_point"]
                # Store the x, y, z values as a list
                center_points[index] = [cp["x"], cp["y"], cp["z"]]

            # Print the results in the desired format
            for i, cp in enumerate(center_points):
                print(f"center_point[{i}] = {cp}")
            
            return center_points
        except json.JSONDecodeError as e:
            self.get_logger().error(f"JSON parsing error: {e}")
            return []

    def send_post_request(self, pcd_file, bmp_file):
        """Send the PCD and PNG files via a POST request to a Docker container."""
        url = "http://localhost:5000/process"
        files = {
            "image": ("image.png", open(bmp_file, 'rb'), "image/png"),
            "pcd": ("pcd.pcd", open(pcd_file, 'rb'), "application/octet-stream")
        }
        
        try:
            response = requests.post(url, files=files)
            # self.get_logger().info(f"Response from server: {response.status_code}, {response.text}")
            return True, response.text
        except Exception as e:
            self.get_logger().error(f"Failed to send POST request: {str(e)}")
            return False, str(e)
        finally:
            files["image"][1].close()
            files["pcd"][1].close()

    def publish_bolt_detection_result(self):
        """Creates and publishes BoltDetectionResult message if new data is available."""
        if not self.latest_result:
            # self.get_logger().warn("No new bolt detection result available.")
            return
        
        center_points = self.extract_center_points(self.latest_result)
        # objects_list = center_points["objects"]
        # self.get_logger().info(f"Objects_inLIST: {objects_list}")
    

        if not center_points:
            # self.get_logger().warn("No bolt center points found.")
            return
        
        center_point_list = []
        for i, cp in enumerate(center_points):
            # print(f"center_point[{i}] = {cp}")
            center_point_list.append(cp)

        result_msg = Float64MultiArray()

        # length = 1   
        length = len(center_point_list)    
        for i in range(length):
            # i = 0
            result_msg.data = center_points[i]  # Store X, Y, Z coordinates
            self.get_logger().info(f"Publishing Bolt #{i}: {center_points[i]}")  # Log the hole coordinates
            self.publisher_.publish(result_msg)
            time.sleep(15)            

      
        # Clear latest result after publishing
        # result_msg.data = center_points[2]
        # self.publisher_.publish(result_msg)
        self.latest_result = None

def main(args=None):
    rclpy.init(args=args)
    node = BoltDetectionNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
