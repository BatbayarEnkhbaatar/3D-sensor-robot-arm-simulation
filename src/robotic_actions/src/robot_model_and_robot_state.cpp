#include <moveit/robot_model_loader/robot_model_loader.h>
#include <moveit/robot_model/robot_model.h>
#include <moveit/robot_state/robot_state.h>
#include <rclcpp/rclcpp.hpp>
#include <eigen3/Eigen/Geometry> // For Eigen::Isometry3d
#include <moveit/move_group_interface/move_group_interface.h>

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::NodeOptions node_options;
  node_options.automatically_declare_parameters_from_overrides(true);
  auto node = rclcpp::Node::make_shared("robotic_actions", node_options);
  const auto& LOGGER = node->get_logger();

  // Load the RobotModel
  robot_model_loader::RobotModelLoader robot_model_loader(node);
  const moveit::core::RobotModelPtr& kinematic_model = robot_model_loader.getModel();
  RCLCPP_INFO(LOGGER, "Model frame: %s", kinematic_model->getModelFrame().c_str());

  // Create RobotState
  moveit::core::RobotStatePtr robot_state(new moveit::core::RobotState(kinematic_model));
  robot_state->setToDefaultValues();
  const moveit::core::JointModelGroup* joint_model_group = kinematic_model->getJointModelGroup("arm");
  auto arm_group = moveit::planning_interface::MoveGroupInterface(node, "arm");
  auto current_pose = arm_group.getCurrentPose("link_t");
  RCLCPP_INFO(LOGGER, "End-Effector Position:\nx: %.3f, y: %.3f, z: %.3f",
            current_pose.pose.position.x,
            current_pose.pose.position.y,
            current_pose.pose.position.z);

  RCLCPP_INFO(LOGGER, "End-Effector Orientation:\nx: %.3f, y: %.3f, z: %.3f, w: %.3f",
            current_pose.pose.orientation.x,
            current_pose.pose.orientation.y,
            current_pose.pose.orientation.z,
            current_pose.pose.orientation.w);


  RCLCPP_INFO(LOGGER, "Current Joint Values get done is");

  // Set joint values and check bounds
  std::vector<double> joint_values;
  robot_state->copyJointGroupPositions(joint_model_group, joint_values);

  joint_values[0] = 2.085;
  joint_values[1] = 2.1337;
  joint_values[2] = -0.7977;
  joint_values[3] = -3.17;
  joint_values[4] = -0.610;
  joint_values[5] = -2.17;
  robot_state->setJointGroupPositions(joint_model_group, joint_values);

  robot_state->enforceBounds();
  RCLCPP_INFO_STREAM(LOGGER, "Current state is " << (robot_state->satisfiesBounds() ? "valid" : "not valid"));

  // Forward Kinematics
  robot_state->setToRandomPositions(joint_model_group);
  const Eigen::Isometry3d& end_effector_state = robot_state->getGlobalLinkTransform("robotiq_85_base_link");

  // Get XYZ and RPY values
  Eigen::Vector3d translation = end_effector_state.translation();
  Eigen::Matrix3d rotation = end_effector_state.rotation();

  // Compute roll, pitch, and yaw from rotation matrix
  Eigen::Vector3d rpy = rotation.eulerAngles(2, 1, 0); // ZYX order: roll (x), pitch (y), yaw (z)
  RCLCPP_INFO_STREAM(LOGGER, "Compute roll, pitch, and yaw from rotation matrix:");
  RCLCPP_INFO_STREAM(LOGGER, "End-effector pose:");
  RCLCPP_INFO_STREAM(LOGGER, "Translation (XYZ): \n" << translation.transpose());
  RCLCPP_INFO_STREAM(LOGGER, "Rotation (RPY): \n" << rpy.transpose());


  std::vector<double> jointVal;
  jointVal = arm_group.getCurrentJointValues();
  for (size_t i = 0; i < jointVal.size(); ++i) {
            RCLCPP_INFO(LOGGER, "Joint %zu: %f", i, jointVal[i]);
        }

 

  // Inverse Kinematics
  // double timeout = 0.1;
  // bool found_ik = robot_state->setFromIK(joint_model_group, end_effector_state, timeout);

  // Create MoveGroupInterface
  // moveit::planning_interface::MoveGroupInterface move_group(node, "arm");
  // Set the target pose
  // geometry_msgs::msg::Pose target_pose;
  // target_pose.position.x = translation.x();
  // target_pose.position.y = translation.y();
  // target_pose.position.z = translation.z();
  
  // Convert RPY to quaternion for target pose
  // Eigen::Quaterniond quaternion = Eigen::AngleAxisd(rpy.z(), Eigen::Vector3d::UnitZ()) *
                                  // Eigen::AngleAxisd(rpy.y(), Eigen::Vector3d::UnitY()) *
                                  // Eigen::AngleAxisd(rpy.x(), Eigen::Vector3d::UnitX());
  // target_pose.orientation.x = quaternion.x();
  // target_pose.orientation.y = quaternion.y();
  // target_pose.orientation.z = quaternion.z();
  // target_pose.orientation.w = quaternion.w();
  
  // move_group.setPoseTarget(target_pose);
  // RCLCPP_INFO(LOGGER, "POSE IS SET.. ");
  // move_group.setPlanningTime(10.0);
  // RCLCPP_INFO(LOGGER, "Planning time out is set by 10s");
  // Plan and execute the motion
  // moveit::planning_interface::MoveGroupInterface::Plan plan;
  // bool success = (move_group.plan(plan) == moveit::core::MoveItErrorCode::SUCCESS);

  // if (success)
  // {
  //   move_group.execute(plan);
  //   RCLCPP_INFO(LOGGER, "Motion executed successfully.");
  // }
  // else
  // {
  //   RCLCPP_ERROR(LOGGER, "Motion execution failed.");
  // }

  // if (found_ik)
  // {
  //   robot_state->copyJointGroupPositions(joint_model_group, joint_values);
  //   for (std::size_t i = 0; i < joint_model_group->getVariableNames().size(); ++i)
  //   {
  //     RCLCPP_INFO(LOGGER, "Joint %s: %f ", joint_model_group->getVariableNames()[i].c_str(), joint_values[i]);
  //   }
  // }
  // else
  // {
  //   RCLCPP_INFO(LOGGER, "Did not find IK solution");
  // }

  // Get the Jacobian
  Eigen::Vector3d reference_point_position(0.0, 0.0, 0.0);
  Eigen::MatrixXd jacobian;
  robot_state->getJacobian(joint_model_group, robot_state->getLinkModel(joint_model_group->getLinkModelNames().back()),
                           reference_point_position, jacobian);
  RCLCPP_INFO_STREAM(LOGGER, "Jacobian: \n" << jacobian << "\n");

  rclcpp::shutdown();
  return 0;
}
