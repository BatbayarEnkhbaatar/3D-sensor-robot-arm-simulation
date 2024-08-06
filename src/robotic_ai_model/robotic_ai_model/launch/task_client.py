from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    taskclientnode = Node(
        package= "robotic_ai_model",
        executable="task_client"
    )
    return LaunchDescription([
        taskclientnode,
])