from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
import os
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("yaskawa_mh5_description"), 
            "launch", 
            "gazebo.launch.py")
    )
    moveit = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("yaskawa_resource_moveit_config"), 
            "launch", 
            "moveit.launch.py")
    )
    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("yaskawa_mh5_controller"), 
            "launch", 
            "controller.launch.py"),
            launch_arguments={"is_sim": "True" }.items()
    )
    # fs100_launch =  IncludeLaunchDsscription (
    #     os.path.join(
    #         get_package_share_directory("fs100_controller_py"),
    #         "launch",
    #         "demo.launch.py"
    #     )
    # )

    return LaunchDescription([
            gazebo,
            moveit,
            controller
    ])
