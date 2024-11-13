from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
import os
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
def generate_launch_description():

            # Load  ExecuteTaskSolutionCapability so we can execute found solutions in simulation
    move_group_capabilities = {
        "capabilities": "move_group/ExecuteTaskSolutionCapability"
    }
    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True",
        description="Whether to use simulation or real hardware"
    )

    moveit_config = MoveItConfigsBuilder("yaskawa_resource").to_moveit_configs()
    rviz_config_file = (
        get_package_share_directory("robotic_actions") + "/launch/move_group.rviz"
    )
    
    moveit_group_node_kinametics_compute = Node(
        package="robotic_actions",
        executable="robot_model_and_robot_state",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
        ],
    )

    return LaunchDescription([moveit_group_node_kinametics_compute])