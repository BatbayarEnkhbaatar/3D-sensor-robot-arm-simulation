import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
import os
import sys
from robotic_msgs.action import YaskawaTasks  

# Add module path for fs100_controller_py
test_dir = os.path.dirname(os.path.realpath(__file__))
module_dir = os.path.dirname(test_dir)
sys.path.append(module_dir)
from fs100_controller_py.fs100 import FS100 

# Initialize the FS100 controller
robot_controller = FS100(ip="10.0.0.2")

class FS100ActionServer(Node):
    
    def __init__(self):
        super().__init__('fs100')
        self._action_server = ActionServer(
            self,
            YaskawaTasks,
            'YaskawaTasks',
            self.execute_callback)
        self.get_logger().info("YASKAWA ROBOT ARM, FS100 CONTROLLER is ready to ...")
        

    def execute_callback(self, goal_handle):
        self.get_logger().info('Received the Robotic Sequences...')
        position = goal_handle.request.task_sequences
        transformed_goal = [
                    int(position[0] * 3*100000),
                    int(position[1] * 3*100000),
                    int(position[2] * (-1123)* 100000),
                    int(position[3] * 58974* 10000),
                    int(position[4] * 120 * 0000),
                    int(position[5] * 1374* 10000),
                ]
        transformed_goal.extend([0,0])
        self.get_logger().info(f"Received Coordinates: {str(position)}")
        self.get_logger().info(f"Transferred Coordinates: {str(transformed_goal)}")
        # Move to the specified position
        self.move_to_position(
            move_type=FS100.MOVE_TYPE_LINEAR_ABSOLUTE_POS,
            coordinate=FS100.MOVE_COORDINATE_SYSTEM_ROBOT,
            speed_class=FS100.MOVE_SPEED_CLASS_MILLIMETER,
            speed=3000,
            position=transformed_goal
        )
        
        goal_handle.succeed()
        result = YaskawaTasks.Result()
        result.success = True
        return result

    def move_to_position(self, move_type, coordinate, speed_class, speed, position):
        # Use the global `robot_controller` instance for moving the robot
        result = robot_controller.mov(
            move_type=move_type,
            coordinate=coordinate,
            speed_class=speed_class,
            speed=speed,
            pos=position
        )
        print(f"Command result: {robot_controller.errno}")
        
        if result == robot_controller.ERROR_SUCCESS:
            print("The command succeeded. RESULT:", result)
        else:
            print(f"Failed to move. Error code: {robot_controller.errno}, Position: {position}")
        
        return result 


def main(args=None):
    rclpy.init(args=args)
    fs100_action_server = FS100ActionServer()
    rclpy.spin(fs100_action_server)
    fs100_action_server.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
