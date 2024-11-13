from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
import os
def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("yaskawa_resource").to_moveit_configs()
    # moveit_config = (
    #     MoveItConfigsBuilder("yaskawa_mh5lf", package_name="yaskawa_resource_moveit_config")
    #     .robot_description(file_path=os.path.join(get_package_share_directory("yaskawa_mh5_description"), "urdf", "mh5.urdf.xacro"))
    #     .robot_description_semantic(file_path="config/yaskawa_mh5lf.srdf")
    #     .trajectory_execution(file_path="config/moveit_controllers.yaml")
    #     .planning_pipelines(pipelines=["ompl"])
    #     ).to_moveit_configs()
    use_sim_time_param = {"use_sim_time": True}
    # Set planning pipeline parameters
    moveit_config.planning_pipelines["ompl"]["arm"][
        "enforce_constrained_state_space"
    ] = True
    moveit_config.planning_pipelines["ompl"]["arm"][
        "projection_evaluator"] = "joints(joint_b ,joint_l)"
    moveit_config.planning_pipelines["ompl"]["arm"]["projection_evaluator"] = "joints(joints(joint_b ,joint_l)"

    run_move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict()],
    )

    action_server_node = Node(
        package="robotic_actions",
        executable="task_server_xyzrpy_node",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            use_sim_time_param
        ],
    )

    return LaunchDescription([action_server_node])