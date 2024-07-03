from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    taskservernode = Node(
        package= "robotic_actions",
        executable="taskservernode"
    )

    rest_api =Node(
        package="robotic_actions",
        executable="rest_api.py"
    )
    return LaunchDescription([
        taskservernode,
        rest_api
])