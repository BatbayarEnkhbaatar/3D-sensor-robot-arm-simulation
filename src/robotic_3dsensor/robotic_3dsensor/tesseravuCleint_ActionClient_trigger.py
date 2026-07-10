import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class DataCaptureClient(Node):
    def __init__(self):
        super().__init__('data_capture_client')
        self.cli = self.create_client(Trigger, 'trigger_data_capture')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        self.send_request()

    def send_request(self):
        req = Trigger.Request()
        future = self.cli.call_async(req)
        future.add_done_callback(self.callback)

    def callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"Success: {response.success}, Message: {response.message}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {str(e)}")


def main(args=None):
    rclpy.init(args=args)
    node = DataCaptureClient()
    rclpy.spin_once(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
