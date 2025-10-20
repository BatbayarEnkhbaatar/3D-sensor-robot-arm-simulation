import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import os
import sys
import time
from robotic_msgs.action import YaskawaTasks

# Add module path for fs100_controller_py
test_dir = os.path.dirname(os.path.realpath(__file__))
module_dir = os.path.dirname(test_dir)
sys.path.append(module_dir)
from fs100_controller_py.fs100 import FS100


class FS100iActionClient(Node):
    def __init__(self):
        super().__init__('fs100_action_client')
        self._action_client = ActionClient(self, YaskawaTasks, 'YaskawaTasks')
        self.goal = YaskawaTasks.Goal()
        self.get_logger().info("Action client is started...")

    def send_goal(self, target_position):
        """Send the goal to the action server."""
        # Set the target position
        self.goal.task_sequences = [float(x) for x in target_position]

        # Send the goal asynchronously
        self.future = self._action_client.send_goal_async(self.goal, feedback_callback=self.feedbackCallback)
        self.future.add_done_callback(self.responseCallback)
    
    def responseCallback(self, future):
        """Callback for goal response."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal Rejected")
            return
        self.get_logger().info("Goal Accepted")
        self.future = goal_handle.get_result_async()
        self.future.add_done_callback(self.resultCallback)

    def resultCallback(self, future):
        """Callback for result."""
        result = future.result().result
        if result.success:
            self.get_logger().info(f"Result: succeed, Feedback: {result.success}")
        else:
            self.get_logger().info("Goal failed")

    def feedbackCallback(self, feedback_msg):
            """Callback for receiving feedback."""
            feedback = feedback_msg.feedback
            self.get_logger().info(f"Received feedback: {feedback.feedbackmsg}")

def main(args=None):
    # Define the positions as lists of floats
    initial_pose = (570000.0, 2665.0, 435800.0, -900000.0, 0.0, -900000.0, 0.0, 0.0)
    pickup = (736090, 3501, -47096, 1310118, -66151, 848797, 0, 0)
    place = (378560.0, 617966.0, -129851.0, 1436337.0, 0.0, -315067.0, 0.0, 0.0)
    
    positions = [initial_pose, pickup, initial_pose, place]

    rclpy.init(args=args)
    action_client = FS100iActionClient()
    current_index = 0
    while rclpy.ok():
            # Send the current position
            if current_index == 2:
                time.sleep(5)
                action_client.get_logger().info(f"Sending position {current_index + 1}: {positions[current_index]}")
                action_client.goal_completed = False
                action_client.send_goal(positions[current_index])
            time.sleep(2)
            action_client.get_logger().info(f"Sending position {current_index + 1}: {positions[current_index]}")
            action_client.goal_completed = False
            action_client.send_goal(positions[current_index])
            # Wait for the action to complete before proceeding
            # while not action_client.goal_completed and rclpy.ok():
            #     rclpy.spin_once(action_client)
      
            # Move to the next position in the list
            current_index += 1
            # If all positions are done, reset to the first position
            if current_index >= len(positions):
                current_index = 0
            # Delay before sending the next goal
            


    rclpy.shutdown()


if __name__ == '__main__':
    main()
