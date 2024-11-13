from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
def generate_launch_description():
    move_group_capabilities = {
        "capabilities": "move_group/ExecuteTaskSolutionCapability"
    }
    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True",
        description="Whether to use simulation or real hardware"
    )
    
    moveit_config = (
        MoveItConfigsBuilder("yaskawa_resource")
        .robot_description(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_description"), "urdf", "mh5.urdf.xacro"))
        .robot_description_semantic(file_path="config/yaskawa_resource.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )

    action_server_node = Node(
        package="robotic_actions",
        executable="motion_planning_api",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            {"use_sim_time": LaunchConfiguration('is_sim')},
            move_group_capabilities],
            arguments=["--ros-args", "--log-level", "info"],
    )

    return LaunchDescription([is_sim_arg, action_server_node])