from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
import os

def generate_launch_description():

    file_transfer_server = Node(
        package="robotic_3dsensor",
        executable="ftp_client_node_ActionClient"
    )


    return LaunchDescription([
            file_transfer_server
    ])
