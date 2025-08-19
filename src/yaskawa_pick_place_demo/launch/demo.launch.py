# launch/pick_place_demo.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    moveit2 = get_package_share_directory("yaskawa_mh5_moveit2")
    robot_description = get_package_share_directory("yaskawa_mh5_description")  # adjust if different
    use_sim = {'use_sim_time': True}
    urdf_xacro = os.path.join(robot_description, "urdf", "mh5.urdf.xacro")
    srdf_file  = os.path.join(moveit2, "config", "yaskawa_mh5lf.srdf")  # adjust filename/path

    # Load SRDF file text
    with open(srdf_file, "r") as f:
        srdf_text = f.read()

    robot_description = {"robot_description": Command(["xacro ", urdf_xacro])}
    robot_description_semantic = {"robot_description_semantic": srdf_text}

    # (Optional) robot_state_publisher for TFs
    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[use_sim, robot_description]
    )

    demo = Node(
        package="yaskawa_pick_place_demo",          # your package
        executable="yaskawa_pick_place_demo",       # your node target
        output="screen",
        parameters=[
            use_sim,
            robot_description,
            robot_description_semantic,
            # your existing parameters:
            {"arm_group": "arm"},
            {"target_state": "pickup"},
            {"lift_state": "lift_up"},
            {"gripper_action": "/task_server_gripper"},
            {"model1_name": "yaskawa_mh5lf"},
            {"link1_name": "robotiq_85_left_finger_tip_link"},
            {"model2_name": "dynamic_object"},
            {"link2_name": "unit_box_link"},
        ],
        )
    robot_semantic    = {"robot_description_semantic": srdf_text}
    logger = Node(
        package="yaskawa_mh5_task_node",                 # your package with the node
        executable="eef_pose_printer_node",       # the target built from the cpp above
        output="screen",
        parameters=[
            robot_description,
            robot_semantic,
            {"group_name": "arm"},
            {"file_path": "/tmp/eef_pose.jsonl"},
            {"rate_hz": 5.0},
            {"gripper_joint": "robotiq_85_left_knuckle_joint"},
            {"use_sim_time": True},                      # if you run Gazebo/MoveIt in sim time
        ],)

    return LaunchDescription([rsp, demo, logger])
