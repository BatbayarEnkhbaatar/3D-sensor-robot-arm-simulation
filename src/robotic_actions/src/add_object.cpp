#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/display_robot_state.hpp>
#include <moveit_msgs/msg/display_trajectory.hpp>
#include <moveit_msgs/msg/attached_collision_object.hpp>
#include <moveit_msgs/msg/collision_object.hpp>
#include <moveit_visual_tools/moveit_visual_tools.h>

static const rclcpp::Logger LOGGER = rclcpp::get_logger("move_group_demo");

int main(int argc, char** argv)
{

  rclcpp::init(argc, argv);
  rclcpp::NodeOptions node_options;
  node_options.automatically_declare_parameters_from_overrides(true);
  auto move_group_node = rclcpp::Node::make_shared("move_group_interface", node_options);

  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(move_group_node);
  std::thread([&executor]() { executor.spin(); }).detach();
 
  static const std::string PLANNING_GROUP = "arm";
  static const std::string PLANNING_GROUP2 = "gripper";

  moveit::planning_interface::MoveGroupInterface move_group(move_group_node, PLANNING_GROUP);
  moveit::planning_interface::MoveGroupInterface move_group2(move_group_node, PLANNING_GROUP2);

  moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

  // Raw pointers are frequently used to refer to the planning group for improved performance.
  const moveit::core::JointModelGroup* joint_model_group =
      move_group.getCurrentState()->getJointModelGroup(PLANNING_GROUP);
  const moveit::core::JointModelGroup* gripper_model_group =
      move_group.getCurrentState()->getJointModelGroup(PLANNING_GROUP2);
  // Visualization
  // ^^^^^^^^^^^^^
  namespace rvt = rviz_visual_tools;
  moveit_visual_tools::MoveItVisualTools visual_tools(move_group_node, "base_link", "move_group",
                                                      move_group.getRobotModel());

  visual_tools.deleteAllMarkers();

  /* Remote control is an introspection tool that allows users to step through a high level script */
  /* via buttons and keyboard shortcuts in RViz */
  visual_tools.loadRemoteControl();

  // RViz provides many types of markers, in this demo we will use text, cylinders, and spheres
  Eigen::Isometry3d text_pose = Eigen::Isometry3d::Identity();
  text_pose.translation().z() = 1.5;
  visual_tools.publishText(text_pose, "MoveGroupInterface_Demo", rvt::WHITE, rvt::XLARGE);

  // Batch publishing is used to reduce the number of messages being sent to RViz for large visualizations
  visual_tools.trigger();

  // Getting Basic Information
  // ^^^^^^^^^^^^^^^^^^^^^^^^^
  //
  // We can print the name of the reference frame for this robot.
  RCLCPP_INFO(LOGGER, "Planning frame: %s", move_group.getPlanningFrame().c_str());

  // We can also print the name of the end-effector link for this group.
  RCLCPP_INFO(LOGGER, "End effector link: %s", move_group.getEndEffectorLink().c_str());

  // We can get a list of all the groups in the robot:
  RCLCPP_INFO(LOGGER, "Available Planning Groups:");
  std::copy(move_group.getJointModelGroupNames().begin(), move_group.getJointModelGroupNames().end(),
            std::ostream_iterator<std::string>(std::cout, ", "));

  // Start the demo
  // ^^^^^^^^^^^^^^^^^^^^^^^^^
  visual_tools.prompt("Press 'next' in the RvizVisualToolsGui window to start the DEMO");


//Add object
  moveit_msgs::msg::CollisionObject collision_object;
  collision_object.header.frame_id = move_group.getPlanningFrame();

  shape_msgs::msg::SolidPrimitive primitive;
  
  std::vector<moveit_msgs::msg::CollisionObject> collision_objects;
  collision_objects.push_back(collision_object);

    moveit_msgs::msg::CollisionObject object_to_attach;
  object_to_attach.id = "cylinder1";

  shape_msgs::msg::SolidPrimitive cylinder_primitive;
  cylinder_primitive.type = primitive.CYLINDER;
  cylinder_primitive.dimensions.resize(2);
  cylinder_primitive.dimensions[primitive.CYLINDER_HEIGHT] = 0.3;
  cylinder_primitive.dimensions[primitive.CYLINDER_RADIUS] = 0.02;

  geometry_msgs::msg::Pose cylinder_pose;
  cylinder_pose.position.x = 1.45;  
  cylinder_pose.position.y = 0.0;  
  cylinder_pose.position.z = 0.075;  
  cylinder_pose.orientation.w = 1.0; 

// Set the pose in the CollisionObject
object_to_attach.primitive_poses.push_back(cylinder_pose);

// Specify that the object is to be attached to a frame (e.g., world frame)
object_to_attach.header.frame_id = "world";

// Indicate that the object is being added
object_to_attach.operation = moveit_msgs::msg::CollisionObject::ADD;

  object_to_attach.primitives.push_back(cylinder_primitive);

  planning_scene_interface.addCollisionObjects(collision_objects);
  planning_scene_interface.applyCollisionObject(object_to_attach);


  visual_tools.publishText(text_pose, "The_object_is_added", rvt::WHITE, rvt::XLARGE);
  visual_tools.trigger();
  visual_tools.prompt("click next ..");

  bool success = false;
  int attempt = 0;
  const int max_attempts = 10;

  moveit_msgs::msg::OrientationConstraint ocm;
  ocm.link_name = "robotiq_85_left_inner_knuckle_link";
  ocm.header.frame_id = "base_link";
  ocm.orientation.w = 1.0;
  // ocm.orientation.x = 1.0;
  // ocm.orientation.y = 0.0;
  // ocm.orientation.z = 0.0;
  // ocm.orientation.w = 0.0;
  ocm.absolute_x_axis_tolerance = 0.01;
  ocm.absolute_y_axis_tolerance = 0.01;
  ocm.absolute_z_axis_tolerance = 0.01;
  ocm.weight = 1.0;

  //Cartesion Path Planning  
  moveit_msgs::msg::Constraints test_constraints;
  test_constraints.orientation_constraints.push_back(ocm);
  move_group.setPathConstraints(test_constraints);

  geometry_msgs::msg::Pose target_pose2;
  target_pose2.position.x = 1.35;
  target_pose2.position.y = 0.0;
  target_pose2.position.z = 0.22;

  std::vector<geometry_msgs::msg::Pose> waypoints;
  waypoints.push_back(target_pose2);

  moveit_msgs::msg::RobotTrajectory trajectory;
  const double jump_threshold = 0.0;
  const double eef_step = 0.0005;
  double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
  RCLCPP_INFO(LOGGER, "Visualizing the plan  to grasp the object (Cartesian path) (%.2f%% achieved)", fraction * 100.0);
 
 //Visualization of Cartesion Path Planning
  visual_tools.deleteAllMarkers();
  visual_tools.publishText(text_pose, "Cartesian_Path", rvt::WHITE, rvt::XLARGE);
  visual_tools.publishPath(waypoints, rvt::LIME_GREEN, rvt::SMALL);
  for (std::size_t i = 0; i < waypoints.size(); ++i)
    visual_tools.publishAxisLabeled(waypoints[i], "pt" + std::to_string(i), rvt::SMALL);
  visual_tools.trigger();
  visual_tools.prompt("Press 'next'  to gasp the object");
  

  //Manipulate the YASKAWA ARM to the target pose
  RCLCPP_INFO(LOGGER, "Approaching the the object to grasp ...");

  move_group.execute(trajectory);

  moveit::planning_interface::MoveGroupInterface::Plan my_plan2;
  bool success_plan2 = false;


  // std::vector<moveit_msgs::Grasp> grasps;
  // grasps.resize(1);
  

std::vector<double> gripper_joint_values = {0.32};  // Gripper joint target value for closing
move_group2.setJointValueTarget(gripper_joint_values);  // Set target values for the gripper joint

moveit::planning_interface::MoveGroupInterface::Plan gripper_plan;
success = false;
attempt = 0;


// move_group2.setGoalTolerance(0.01);  // Optionally set a tolerance (adjust as needed)
move_group2.setPlanningTime(5.0);    // Set planning time (5 seconds)
move_group2.setGoalTolerance(0.001);  // Set a smaller tolerance

while (attempt < max_attempts && !success) {
    // Plan the gripper motion
    success = (move_group2.plan(gripper_plan) == moveit::core::MoveItErrorCode::SUCCESS);
    std::vector<double> current_joint_values = move_group2.getCurrentJointValues();
    for (size_t i = 0; i < current_joint_values.size(); ++i) {
        RCLCPP_INFO(LOGGER, "Current Joint %ld: %f", i, current_joint_values[i]);
    }



    if (success) {
        RCLCPP_INFO(LOGGER, "Planning succeeded, ESCEEEEECURINT<...");

        // Execute the planned motion
        moveit::planning_interface::MoveItErrorCode execution_result = move_group2.move();
        
        if (execution_result == moveit::core::MoveItErrorCode::SUCCESS) {
            RCLCPP_INFO(LOGGER, "Gripper closed successfully."); 
            std::vector<std::string> touch_links;
            touch_links.push_back("robotiq_85_left_knuckle_link");
            touch_links.push_back("robotiq_85_right_knuckle_link");
            move_group.attachObject(object_to_attach.id, "robotiq_85_left_knuckle_link", touch_links);

            break;  // Exit the loop if execution succeeded
        } else {
            RCLCPP_ERROR(LOGGER, "Motion execution failed, retrying...");
        }
    } else {
        RCLCPP_ERROR(LOGGER, "Planning failed, retrying...");
    }

    attempt++;
}

if (!success) {
    RCLCPP_ERROR(LOGGER, "Gripper closing failed after %d attempts.", max_attempts);
}
  object_to_attach.header.frame_id = move_group.getEndEffectorLink();
  geometry_msgs::msg::Pose grab_pose;


  visual_tools.publishText(text_pose, "Object_is_attached_to_Gripper_and_next_is_to_close_gripper", rvt::WHITE, rvt::XLARGE);
  visual_tools.trigger();
  visual_tools.prompt("next is the placing the object into another , please click next button to proceed...");


 move_group.setStartState(*move_group.getCurrentState());

  geometry_msgs::msg::Pose place_pose;
  place_pose.orientation.w = 1.0;
  place_pose.position.x = 1.0;
  place_pose.position.y = 0.83;
  place_pose.position.z = 0.22;
  move_group.setGoalTolerance(0.2);
  move_group.setPlanningTime(15);
  move_group.setPoseTarget(place_pose);
  
  moveit::planning_interface::MoveGroupInterface::Plan my_plan3;
  success_plan2 = false;

  waypoints.push_back(place_pose);

  moveit_msgs::msg::RobotTrajectory trajectory2;
  double fraction2 = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory2);
  RCLCPP_INFO(LOGGER, "Visualizing the plan  to grasp the object (Cartesian path) (%.2f%% achieved)", fraction2 * 100.0);
  move_group.execute(trajectory2);
  // Replan, but now with the object in hand.
  move_group.setStartStateToCurrentState();
  success = (move_group.plan(my_plan3) == moveit::core::MoveItErrorCode::SUCCESS);
  RCLCPP_INFO(LOGGER, "Visualizing plan with cylinder %s", success ? "" : "FAILED");
  visual_tools.publishTrajectoryLine(my_plan3.trajectory_, joint_model_group);
  visual_tools.trigger();
  visual_tools.prompt("Press 'next' in the RvizVisualToolsGui window once the plan is complete");
  


  attempt = 0;

  while (attempt < max_attempts) {
      success_plan2 = (move_group.plan(my_plan3) == moveit::core::MoveItErrorCode::SUCCESS);

      if (success_plan2) {
          RCLCPP_INFO(LOGGER, "Moving the the object to new location , Plan succeeded on attempt %d, moving to target.", attempt + 1);
          move_group.move();
          break;
      } else {
          RCLCPP_WARN(LOGGER, "Moving the the object to new location, Plan attempt %d failed, retrying...", attempt + 1);
      }
      attempt++;
  }
  RCLCPP_INFO(LOGGER, "move the cylinder ovject ) %s", success ? "" : "FAILED");
  // visual_tools.publishTrajectoryLine(my_plan3.trajectory, joint_model_group);


  


  move_group.detachObject(object_to_attach.id);

  // Show text in RViz of status
  visual_tools.deleteAllMarkers();
  visual_tools.publishText(text_pose, "Object_detached_from_robot", rvt::WHITE, rvt::XLARGE);
  visual_tools.trigger();
  // RCLCPP_INFO(LOGGER, "Remove the objects from the world");



 move_group.setStartState(*move_group.getCurrentState());

  geometry_msgs::msg::Pose basic_pose;
  basic_pose.orientation.w = 1.0;
  basic_pose.position.x = 1.0;
  basic_pose.position.y = 1.0;
  basic_pose.position.z = 1.0;
  move_group.setGoalTolerance(0.1);
  move_group.setPlanningTime(15);
  move_group.setPoseTarget(basic_pose);
  
  moveit::planning_interface::MoveGroupInterface::Plan my_plan4;
  success_plan2 = false;

  waypoints.push_back(basic_pose);

  moveit_msgs::msg::RobotTrajectory trajectory3;
  double fraction3 = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory3);
  RCLCPP_INFO(LOGGER, "Visualizing the plan  to grasp the object (Cartesian path) (%.2f%% achieved)", fraction3 * 100.0);
  move_group.execute(trajectory3);
  // Replan, but now with the object in hand.
  move_group.setStartStateToCurrentState();
  success = (move_group.plan(my_plan4) == moveit::core::MoveItErrorCode::SUCCESS);
  RCLCPP_INFO(LOGGER, "Visualizing plan with cylinder %s", success ? "" : "FAILED");
  visual_tools.publishTrajectoryLine(my_plan4.trajectory_, joint_model_group);
  visual_tools.trigger();
  visual_tools.prompt("Press 'next' in the RvizVisualToolsGui window once the plan is complete");
  


  rclcpp::shutdown();
  return 0;
}