from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
from launch.substitutions import LaunchConfiguration
import os
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

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

    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True",
        description="Whether to use simulation or real hardware"
    )
    # Create MoveIt configuration
    # moveit_config = (
    #     MoveItConfigsBuilder("yaskawa_mh5lf", package_name="yaskawa_mh5_moveit2")
    #     .robot_description(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_description"), "urdf", "mh5.urdf.xacro"))
    #     .robot_description_semantic(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_moveit2"), "config", "yaskawa_mh5lf.srdf"))
    #     .trajectory_execution(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_moveit2"), "config", "moveit_controllers.yaml"))
    #     .robot_description_kinematics(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_moveit2"), "config", "kinematics.yaml"))
    #     .to_moveit_configs()
    # )
    moveit_config = (
        MoveItConfigsBuilder("yaskawa_mh5lf", package_name="yaskawa_mh5_moveit2")
        .robot_description(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_description"), "urdf", "mh5.urdf.xacro"))
        .robot_description_semantic(file_path="config/yaskawa_mh5lf.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
    )
    pipeline_params = {
        "planning_pipelines": ["ompl"],          # available pipelines
        "default_planning_pipeline": "ompl",     # pick OMPL by default
    }
    pkg_mtc = get_package_share_directory("yaskawa_mh5_moveit2")

    # Create Move Group node
    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict(), {"use_sim_time": LaunchConfiguration('is_sim')}, {"publish_robot_description_semantic": True}, 
                    os.path.join(pkg_mtc, "config", "pipelines_ompl.yaml"),],
        arguments=["--ros-args", "--log-level", "info"]
    )
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


    # your task server (the node that calls MoveGroupInterface)
    task_server = Node(
        package="yaskawa_mh5_task_node",
        executable="task_server_arm_node",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            {"use_sim_time": is_sim},
            move_group_capabilities],
        arguments=["--ros-args", "--log-level", "debug"],
    )


    

    return LaunchDescription([
            gazebo,
            controller,
            moveit,
            move_group,

    ])
