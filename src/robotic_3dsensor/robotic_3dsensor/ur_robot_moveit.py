#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from moveit2 import MoveIt2

class URMoveItController(Node):
    def __init__(self):
        super().__init__('ur_moveit_controller')
        self.moveit2 = MoveIt2(node=self, joint_names=['shoulder_pan_joint', 'shoulder_lift_joint',
                                                       'elbow_joint', 'wrist_1_joint',
                                                       'wrist_2_joint', 'wrist_3_joint'],
                               base_link_name='base_link',
                               end_effector_name='tool0',
                               group_name='ur_manipulator',
                               execute=True)

    def move_to_pose(self, pose: PoseStamped):
        self.moveit2.move_to_pose(pose)

def main(args=None):
    rclpy.init(args=args)
    node = URMoveItController()

    target_pose = PoseStamped()
    target_pose.header.frame_id = 'base_link'
    target_pose.pose.position.x = 0.4
    target_pose.pose.position.y = 0.0
    target_pose.pose.position.z = 0.4
    target_pose.pose.orientation.w = 1.0

    node.move_to_pose(target_pose)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
