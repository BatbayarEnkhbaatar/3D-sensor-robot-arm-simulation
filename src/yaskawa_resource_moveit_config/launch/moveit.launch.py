from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder
import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node


def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return yaml.safe_load(file)
    except EnvironmentError:
        return None


def generate_launch_description():
    
    # Argument to select simulation or real hardware
    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True",
        description="Whether to use simulation or real hardware"
    )

    # Load MoveIt configurations for Yaskawa MH5LF robot
    moveit_config = (
        MoveItConfigsBuilder("yaskawa_mh5lf", package_name="yaskawa_resource_moveit_config")
        .robot_description(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_description"), "urdf", "mh5.urdf.xacro"))
        .robot_description_semantic(file_path=os.path.join(get_package_share_directory("yaskawa_resource_moveit_config"), "config", "yaskawa_resource.srdf"))
        .trajectory_execution(file_path=os.path.join(get_package_share_directory("yaskawa_resource_moveit_config"), "config", "moveit_controllers.yaml"))
        .planning_pipelines(pipelines=["ompl", "pilz_industrial_motion_planner"])  # Load both OMPL and Pilz planners
        .to_moveit_configs()
    )

    # Capabilities for move_group
    move_group_capabilities = {
        "capabilities": "move_group/ExecuteTaskSolutionCapability"
    }

    # Create Move Group node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": LaunchConfiguration('is_sim')},
            move_group_capabilities
        ],
        arguments=["--ros-args", "--log-level", "info"],
    )
    
    # Create RViz node for visualization
    rviz_config = os.path.join(get_package_share_directory("yaskawa_resource_moveit_config"), "config", "moveit.rviz")

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[
            {"use_sim_time": LaunchConfiguration('is_sim')},  # Ensure sim time is passed here as well
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            moveit_config.trajectory_execution
        ]
    )

    return LaunchDescription([
        is_sim_arg,
        move_group_node,
        rviz_node,
    ])
