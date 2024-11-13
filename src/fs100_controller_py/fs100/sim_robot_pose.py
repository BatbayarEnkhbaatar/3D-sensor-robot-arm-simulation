import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import GetModelState


class GazeboModelStateClient(Node):
    def __init__(self):
        super().__init__('gazebo_model_state_client')
        self.cli = self.create_client(GetModelState, '/gazebo/get_model_state')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /gazebo/get_model_state service...')
        self.request = GetModelState.Request()

    def get_model_position(self, model_name, relative_entity_name='world'):
        self.request.model_name = model_name
        self.request.relative_entity_name = relative_entity_name
        
        self.future = self.cli.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.future)
        
        if self.future.result() is not None:
            model_state = self.future.result()
            if model_state.success:
                self.get_logger().info(f"Position of {model_name}: x={model_state.pose.position.x}, "
                                       f"y={model_state.pose.position.y}, z={model_state.pose.position.z}")
                return model_state.pose.position
            else:
                self.get_logger().error(f"Failed to get model state: {model_state.status_message}")
        else:
            self.get_logger().error("Service call failed")
        return None


def main(args=None):
    rclpy.init(args=args)
    node = GazeboModelStateClient()

    model_name = 'Yaskawa'  # Replace with your model's name in Gazebo
    node.get_model_position(model_name)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
