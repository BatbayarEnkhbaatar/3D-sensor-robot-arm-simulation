from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
import os

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    task_client_demo = Node(
        package="fs100_controller_py",  
        executable="task_client_demo",
        output = "screen"
    )
    
    task_server_demo = Node(
        package="fs100_controller_py",  
        executable="task_server_demo",
        output = "screen"
    )
    
    return LaunchDescription([
        fs100_task_client_demo,
        fs100_task_server_demo            
    ])
