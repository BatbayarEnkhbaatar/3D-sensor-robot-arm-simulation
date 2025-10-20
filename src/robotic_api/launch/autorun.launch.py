from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():


    # robotic_api_calib = Node(
    #     package = "robotic_api",
    #     executable="tesseravue_ActionClient_api",

    # )
    robotic_api_calib = Node(
        package = "robotic_api",
        executable="tesseravue_ActionClient_api",

    )
    # ur_task_server = Node(
    #     package="ur_robot_task_server",
    #     executable="ur_robot_action_node",
    # )
    fs100_controller_py = Node(
        package="fs100_controller_py",  
        executable="task_server_gripper",
        output = "screen"
    )
    
    task_server_robot = Node(
        package="fs100_controller_py",  
        executable="task_server_robot",
        output = "screen"
    )
    
    return LaunchDescription([

            robotic_api_calib,
            fs100_controller_py,
            task_server_robot
    ])
