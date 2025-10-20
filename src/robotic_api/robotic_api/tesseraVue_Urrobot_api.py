import os
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from ament_index_python.packages import get_package_share_directory
from robotic_msgs.action import TesseraVueTasks
from std_srvs.srv import Trigger
# from robot import controlRobot
from tesseravue import tesseravue_client


class TesseraVueClientNode(Node):
    def __init__(self): 
        super().__init__('tesseraVue_client_node')
        self._action_client = ActionClient(self, TesseraVueTasks, "TesseraVueTasks")
        self.get_logger().info("TesseraVue Client Node is Ready...")

        package_name = 'robotic_api'
        self.package_share_directory = get_package_share_directory(package_name)
        self.local_directory = os.path.join(self.package_share_directory, 'data/')
        os.makedirs(self.local_directory, exist_ok=True)

        # Trigger service to control when get_data runs
        self.srv = self.create_service(Trigger, 'trigger_data_capture', self.trigger_callback)

    def trigger_callback(self, request, response):
        self.get_logger().info("Trigger received: capturing data...")
        self.get_data()
        response.success = True
        response.message = "Data captured and goal sent"
        return response

    def get_data(self):
        try:
            sensor_ip = "192.168.0.10"
            sensor_port = 1024
            img, pcd = tesseravue_client._cli(ip=sensor_ip, tcp=sensor_port, strPath=self.local_directory)
            # pcd = filename + ".pcd"
            # img = filename + ".bmp"
            # path_pcd = os.path.join(self.local_directory, pcd)
            # path_img = os.path.join(self.local_directory, img)
            self.get_logger().info(img)
            self.get_logger().info(pcd)
            self._send_action_goal([pcd, img])
        except Exception as er:
            self.get_logger().error(f"Error capturing data: {str(er)}")

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


def main(args=None):
    rclpy.init(args=args)
    node = TesseraVueClientNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
    # controlRobot.main()
