from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    task_server_node = Node(
        package= "robotic_action",
        executable="task_server_node"
    )

    rest_api_yaskawa =Node(
        package="robotic_action",
        executable="rest_api.py"
    )
    return LaunchDescription([
        task_server_node,
        rest_api_yaskawa
])