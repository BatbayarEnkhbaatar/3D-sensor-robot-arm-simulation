#!/usr/bin/env python3
# File: grasp_demo.py

import math
import rclpy
from rclpy.node import Node
from rclpy.task import Future
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseStamped
from builtin_interfaces.msg import Duration

# MoveIt2 Python interface
from moveit_commander import MoveGroupCommander, PlanningSceneInterface, roscpp_initialize, roscpp_shutdown

# Your action type
from robotic_msgs.action import RoboticGripperTasks

# Gazebo Classic link attacher (optional)
from gazebo_ros_link_attacher.srv import Attach as AttachSrv

class GraspDemo(Node):
    def __init__(self):
        super().__init__('grasp_demo')

        # ---------- CONFIG ----------
        self.arm_group_name = 'manipulator'           # your MoveIt arm group (use your actual group)
        self.base_frame     = 'base_link'             # frame for target poses
        self.eef_link       = ''                      # leave empty to use group's default eef
        # Object pose (center of cube). Adjust Z = table_height + size/2
        self.object_xyz     = (0.75, 0.00, 0.03/2.0)  # for a 3 cm cube on the ground; change if on table
        self.approach_height= 0.10                    # 10 cm above object (pre-grasp)
        self.lift_dist      = 0.10                    # 10 cm lift
        # Gripper action & values (Robotiq 85 rad)
        self.gripper_action = '/gripper_task_server'
        self.grip_open      = 0.00
        self.grip_close     = 0.80
        # Gazebo link attacher (optional) – set to True if you have the plugin loaded
        self.use_attach     = True
        self.attach_srv_ns  = '/link_attacher'
        self.robot_model    = 'yaskawa_mh5lf'
        self.robot_grip_link= 'robotiq_85_left_finger_tip_link'
        self.obj_model      = 'cube'
        self.obj_link       = 'cube_link'
        # ----------------------------

        # MoveIt init
        roscpp_initialize([])
        self.group = MoveGroupCommander(self.arm_group_name)
        if self.eef_link:
            self.group.set_end_effector_link(self.eef_link)
        self.group.set_pose_reference_frame(self.base_frame)
        self.group.set_max_velocity_scaling_factor(0.3)
        self.group.set_max_acceleration_scaling_factor(0.3)
        self.group.set_planning_time(5.0)

        # Gripper action client
        self.grip_client = ActionClient(self, RoboticGripperTasks, self.gripper_action)

        # Attach/detach services
        if self.use_attach:
            self.attach_cli  = self.create_client(AttachSrv, f'{self.attach_srv_ns}/attach')
            self.detach_cli  = self.create_client(AttachSrv, f'{self.attach_srv_ns}/detach')

    # ----------------- Helpers -----------------
    def plan_and_exec(self, target_pose: PoseStamped) -> bool:
        self.group.set_pose_target(target_pose)
        plan = self.group.plan()
        # MoveIt2 in ROS2 may return tuple(plan, frac, desc) or a plan object
        if isinstance(plan, tuple):
            success = plan[0] is not None and len(plan[1].joint_trajectory.points) > 0 if hasattr(plan[1], 'joint_trajectory') else True
            exec_plan = plan[1] if len(plan) > 1 else plan[0]
        else:
            success = plan and hasattr(plan, 'joint_trajectory') and len(plan.joint_trajectory.points) > 0
            exec_plan = plan

        if not success:
            self.get_logger().error('Planning failed.')
            return False

        result = self.group.execute(exec_plan, wait=True)
        self.group.stop()
        self.group.clear_pose_targets()
        return bool(result)

    def make_pose(self, x, y, z, q=(0,0,0,1)) -> PoseStamped:
        p = PoseStamped()
        p.header.frame_id = self.base_frame
        p.pose.position.x = float(x)
        p.pose.position.y = float(y)
        p.pose.position.z = float(z)
        p.pose.orientation.x, p.pose.orientation.y, p.pose.orientation.z, p.pose.orientation.w = q
        return p

    def close_gripper(self, value: float) -> bool:
        if not self.grip_client.wait_for_server(timeout_sec=3.0):
            self.get_logger().error('Gripper action server not available.')
            return False
        goal = RoboticGripperTasks.Goal()
        goal.gripper_command = [float(value)]
        send_future = self.grip_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send_future)
        goal_handle = send_future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Gripper goal rejected.')
            return False
        res_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, res_future)
        res = res_future.result().result
        ok = bool(res.success)
        self.get_logger().info(f'Gripper result: {ok}')
        return ok

    def call_attach(self, attach: bool) -> bool:
        if not self.use_attach:
            return True
        cli = self.attach_cli if attach else self.detach_cli
        if not cli.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn('Attach/detach service not available.')
            return False
        req = AttachSrv.Request()
        req.model_name_1 = self.robot_model
        req.link_name_1  = self.robot_grip_link
        req.model_name_2 = self.obj_model
        req.link_name_2  = self.obj_link
        fut = cli.call_async(req)
        rclpy.spin_until_future_complete(self, fut)
        ok = fut.result() is not None
        self.get_logger().info(('Attached' if attach else 'Detached') + f' = {ok}')
        return ok

    # ----------------- Script -----------------
    def run(self):
        x, y, z_obj = self.object_xyz
        q = (0,0,0,1)  # rpy 0,0,0

        # 1) Pre-grasp above object
        pre = self.make_pose(x, y, z_obj + self.approach_height, q)
        if not self.plan_and_exec(pre): return

        # 2) Approach straight down (Cartesian)
        waypoints = []
        approach = self.make_pose(x, y, z_obj + 0.01, q)  # stop ~1cm above center
        waypoints.append(approach.pose)
        (traj, frac) = self.group.compute_cartesian_path(waypoints, eef_step=0.005, jump_threshold=0.0)
        if frac < 0.99 or not traj.joint_trajectory.points:
            self.get_logger().warn(f'Cartesian approach incomplete (frac={frac:.2f}), attempting execute anyway.')
        self.group.execute(traj, wait=True)

        # 3) Close gripper
        if not self.close_gripper(self.grip_close):
            self.get_logger().error('Failed to close gripper.')
            return

        # 4) Attach in Gazebo (optional but robust)
        self.call_attach(True)

        # 5) Lift
        waypoints = []
        lift = self.make_pose(x, y, z_obj + self.approach_height, q)
        waypoints.append(lift.pose)
        (traj, frac) = self.group.compute_cartesian_path(waypoints, eef_step=0.005, jump_threshold=0.0)
        self.group.execute(traj, wait=True)

        # 6) (Optional) Move somewhere to place – here we just move a bit in +Y
        place = self.make_pose(x, y + 0.15, z_obj + self.approach_height, q)
        self.plan_and_exec(place)

        # 7) Lower
        waypoints = []
        lower = self.make_pose(x, y + 0.15, z_obj + 0.01, q)
        waypoints.append(lower.pose)
        (traj, frac) = self.group.compute_cartesian_path(waypoints, eef_step=0.005, jump_threshold=0.0)
        self.group.execute(traj, wait=True)

        # 8) Detach + open
        self.call_attach(False)
        self.close_gripper(self.grip_open)

        # 9) Retreat up
        waypoints = []
        retreat = self.make_pose(x, y + 0.15, z_obj + self.approach_height, q)
        waypoints.append(retreat.pose)
        (traj, frac) = self.group.compute_cartesian_path(waypoints, eef_step=0.005, jump_threshold=0.0)
        self.group.execute(traj, wait=True)

        self.get_logger().info('Grasp sequence complete.')

def main():
    rclpy.init()
    node = GraspDemo()
    try:
        node.run()
    finally:
        node.destroy_node()
        roscpp_shutdown()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
