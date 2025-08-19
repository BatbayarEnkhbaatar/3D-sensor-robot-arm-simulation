from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from moveit_configs_utils import MoveItConfigsBuilder
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():
    move_group_capabilities = {
        "capabilities": "move_group/ExecuteTaskSolutionCapability"
    }
    is_sim = LaunchConfiguration('is_sim')
    moveit_config = (
        MoveItConfigsBuilder("yaskawa_mh5lf", package_name="yaskawa_mh5_moveit2")
        .robot_description(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_description"), "urdf", "mh5.urdf.xacro"))
        .robot_description_semantic(file_path="config/yaskawa_mh5lf.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
    )
    # your task server (the node that calls MoveGroupInterface)
    get_eef_pose = Node(
        package="yaskawa_mh5_task_node",
        executable="eef_pose_printer_node",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            {"use_sim_time": is_sim},
            move_group_capabilities],
        arguments=["--ros-args", "--log-level", "info"],
    )

    return LaunchDescription([
            get_eef_pose 
    ])
