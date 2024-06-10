from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    task_server_node = Node(
        package= "yaskawa_remote",
        executable="task_server_node"
    )

    rest_api_yaskawa =Node(
        package="yaskawa_remote",
        executable="rest_api_yaskawa.py"
    )
    return LaunchDescription([
        task_server_node,
        rest_api_yaskawa
])