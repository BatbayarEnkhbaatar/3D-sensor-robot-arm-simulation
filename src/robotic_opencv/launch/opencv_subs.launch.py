from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    opencvSubscriberNode = Node(
        package= "robotic_opencv",
        executable="opencv_subscriber_node"
    )
    opencvRemover = Node(
        package= "robotic_opencv",
        executable="maintainerNode"
    )
    return LaunchDescription([
        opencvSubscriberNode,
        opencvRemover

])