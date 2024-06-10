from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
import os

def generate_launch_description():

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("yaskawa_mh5_description"), 
            "launch", 
            "gazebo.launch.py")
    )
    
    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("yaskawa_mh5_controller"), 
            "launch", 
            "controller.launch.py"
            ),
        launch_arguments={"is_sim": "True" }.items()
    )
    moveit = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("yaskawa_mh5_moveit2"), 
            "launch", 
            "moveit.launch.py"),
        launch_arguments={"is_sim": "True" }.items()
    )
    remote_interface = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("yaskawa_remote"), 
            "launch", 
            "remote_interface.launch.py"
            )
    )

    return LaunchDescription([
            gazebo,
            controller,
            moveit,
            remote_interface
    ])
