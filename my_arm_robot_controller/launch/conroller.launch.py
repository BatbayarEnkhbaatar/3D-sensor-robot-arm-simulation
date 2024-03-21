from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

import os
from os import pathsep


def generate_launch_description():
    robot_description = ParameterValue(Command(
        [
            'xacro ', os.path.join(get_package_share_directory("my_arm_robot_description"), "urdf", "model.urdf.xacro")
            ]
            ),
        value_type=str
    )
    robot_state_publisher = Node(
        package = "robot_state_publisher",
        executable = "robot_state_publisher",
        parameters = [{"robot_description": robot_description}]
    ),

    joint_state_broadcaster_spawner = Node(
        package = "joint_state_broadcaster",
        executable = "spawner",
        arguments= [
            "joint_state_broadcaster",
            "--contoller-manager",
            "/controller_manager",
        ]
    )

    joint_state_broadcaster_spawner = Node(
        package = "joint_state_broadcaster",
        executable = "spawner",
        arguments= [
            "joint_state_broadcaster",
            "--contoller-manager",
            "/controller_manager"
        ]
    )
    arm_controller_spawner = Node(
        package = "contoller_manager",
        executable = "spawner",
        arguments= [
            "arm_controller",
            "--contoller-manager",
            "/controller_manager"
        ]
    )
    gripper_controller_spawner = Node(
        package = "contoller_manager",
        executable = "spawner",
        arguments= [
            "gripper_controller",
            "--contoller-manager",
            "/controller_manager"
        ]
    )
    return LaunchDescription([
        robot_state_publisher,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
        gripper_controller_spawner
    ])