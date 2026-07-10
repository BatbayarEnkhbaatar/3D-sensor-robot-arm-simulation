from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():

    hand_eye_calib = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robotic_3dsensor"), 
            "launch", 
            "hand_to_eye_calib.launch.py"),

    )
    bolt_detect = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robotic_bolt_detection"), 
            "launch", 
            "run_bolt_detection.launch.py"
            ),
    )
    ur_task_server = Node(
        package="ur_robot_task_server",
        executable="ur_robot_action_node",
    )
    robotic_3dsensor = Node(
        package="robotic_3dsensor",
        executable="tesseravuCleint_ActionClient_node",
    )


    return LaunchDescription([
            hand_eye_calib,
            ur_task_server,
            bolt_detect,
            robotic_3dsensor
    ])
