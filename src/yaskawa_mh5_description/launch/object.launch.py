from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from os import pathsep

def generate_launch_description():
    
    object_description = get_package_share_directory("point_cloud_processing")
    object_description_prefix = get_package_prefix("point_cloud_processing")
    object_path = os.path.join(object_description, "motoman_resources")
    object_path += pathsep + os.path.join(object_description_prefix, "share")
    env_variable = SetEnvironmentVariable("GAZEBO_MODEL_PATH", object_path)

    object_arg = DeclareLaunchArgument(
            name="models", 
            default_value=os.path.join(get_package_share_directory("point_cloud_processing"), "urdf", "dynamic_object.urdf.xacro"),
            description="Absolute path to the robot URDF file"
        )
    

    object_description = ParameterValue(Command(['xacro ', LaunchConfiguration("models")]))

    object_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": object_description}]
    )

    spawn_object = Node (
        package = "gazebo_ros",
        executable= "spawn_entity.py",
        name = "spawn_object",
        output = "screen",
        arguments= ['-entity', 'dynamic_object',  "-topic", "robot_description"]


    )
    return LaunchDescription([
        env_variable,
        object_arg,
        object_state_publisher_node,
        spawn_object
    ])