from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    ftp_server_node = Node(
        package="robotic_3dsensor",
        executable="ftp_client_node",
        output="screen")
    data_processing_node = Node(
        package="robotic_3dsensor",
        executable="data_processing_node",
        output="screen")

    return LaunchDescription([ftp_server_node, data_processing_node])