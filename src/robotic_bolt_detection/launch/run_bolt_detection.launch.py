from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
def generate_launch_description():
    
    robot_bolt_detection_node = Node(
        package="robotic_bolt_detection",
        executable="bolt_detection_ActionServer",
    )
    return LaunchDescription([
        robot_bolt_detection_node
    ])

