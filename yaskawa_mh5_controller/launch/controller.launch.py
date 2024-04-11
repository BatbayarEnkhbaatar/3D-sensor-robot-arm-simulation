from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
import os

def generate_launch_description():
#     robot_description = ParameterValue(
#     Command(
#         [
#             'xacro ', 
#             os.path.join(get_package_share_directory("yaskawa_mh5_description"), "urdf", "mh5.xacro")
#         ]
#     ),
#     value_type=str
# )
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",  
            "/controller_manager",
        ]
    )
    arm_controller_spawner = Node(
        package="controller_manager",  
        executable="spawner",
        arguments=[
            "arm_controller",
            "--controller-manager", 
            "/controller_manager",
        ]
    )

    return LaunchDescription([
        joint_state_broadcaster_spawner,
        arm_controller_spawner

    ])
