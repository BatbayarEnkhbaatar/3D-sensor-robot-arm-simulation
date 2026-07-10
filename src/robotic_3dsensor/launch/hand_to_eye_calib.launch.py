from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
import os

def generate_launch_description():

    calibration_Eye_to_End = Node(
        package="robotic_3dsensor",
        executable="calibraion_eye2hand_node"
    )


    return LaunchDescription([
            calibration_Eye_to_End
    ])
