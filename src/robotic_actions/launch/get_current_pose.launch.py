from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
import os
def generate_launch_description():

    moveit_config = (
        MoveItConfigsBuilder("yaskawa_mh5lf", package_name="yaskawa_mh5_moveit2")
        .robot_description(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_description"), "urdf", "mh5.urdf.xacro"))
        .robot_description_semantic(file_path="config/yaskawa_resource.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .planning_pipelines(pipelines=["ompl", "chomp", "pilz_industrial_motion_planner"]
        )
        .to_moveit_configs()
    )

    getting_current_pose_node = Node(
        package="robotic_actions",
        executable="sample_task0",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
        ],
        remappings=[
            ("joint_states", "robot/joint_states")
        ]
    )

    return LaunchDescription([getting_current_pose_node])