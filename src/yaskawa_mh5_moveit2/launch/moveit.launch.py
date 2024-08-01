from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from moveit_configs_utils import MoveItConfigsBuilder
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import launch

def generate_launch_description():
    # Declare launch arguments
    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True",
        description="Whether to use simulation or real hardware"
    )

    # gui_arg = DeclareLaunchArgument(
    #     name="gui", 
    #     default_value="False",
    #     description="Enable GUI"
    # )
    
    # Create MoveIt configuration
    moveit_config = (
        MoveItConfigsBuilder("yaskawa_mh5lf", package_name="yaskawa_mh5_moveit2")
        .robot_description(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_description"), "urdf", "mh5.urdf.xacro"))
        .robot_description_semantic(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_moveit2"), "config", "yaskawa_mh5lf.srdf"))
        .trajectory_execution(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_moveit2"), "config", "moveit_controllers.yaml"))
        .to_moveit_configs()
    )

    # Create Move Group node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict(), {"use_sim_time": LaunchConfiguration('is_sim')}, {"publish_robot_description_semantic": True}],
        arguments=["--ros-args", "--log-level", "info"]
    )

    # Create Joint State Publisher node with GUI condition
    # joint_state_publisher_node = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher'
    # )

    # Create RViz node
    rviz_config = os.path.join(get_package_share_directory("yaskawa_mh5_moveit2"), "config", "moveit.rviz")

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits
        ]
    )

    return LaunchDescription([
        is_sim_arg,
        move_group_node,
        rviz_node
    ])
