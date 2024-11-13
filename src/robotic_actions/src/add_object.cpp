#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/display_robot_state.hpp>
#include <moveit_msgs/msg/display_trajectory.hpp>
#include <moveit_msgs/msg/attached_collision_object.hpp>
#include <moveit_msgs/msg/collision_object.hpp>
#include <moveit_visual_tools/moveit_visual_tools.h>
#include <chrono>
static const rclcpp::Logger LOGGER = rclcpp::get_logger("move_group_demo");


void moveToInitialPose_JointAnkle(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                moveit::planning_interface::MoveGroupInterface &move_group_gripper,
                moveit_visual_tools::MoveItVisualTools &visual_tools) {
    // Arm initial pose joint ankle
    std::vector<double> arm_inital_pose = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    move_group_arm.setJointValueTarget(arm_inital_pose);

    moveit::planning_interface::MoveGroupInterface::Plan arm_plan;

     if (move_group_arm.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
        move_group_arm.move();
        RCLCPP_INFO(LOGGER, "Yaskawa ARM in initial pose.");
    } else {
        RCLCPP_ERROR(LOGGER, "Yaskawa ARM failed to get in initial pose");
    }

    // Close the gripper
    std::vector<double> openned_gripper_position = {0.2, -0.2, 0.2, -0.2, 0.2, -0.2};
    move_group_gripper.setJointValueTarget(openned_gripper_position);
    moveit::planning_interface::MoveGroupInterface::Plan gripper_plan;
    if (move_group_gripper.plan(gripper_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
        move_group_gripper.move();
        RCLCPP_INFO(LOGGER, "Gripper openned successfully.");
    } else {
        RCLCPP_ERROR(LOGGER, "Failed to plan the gripper openning motion.");
    }
     visual_tools.trigger();  // Update RViz visualization
}

void moveToInitialPose(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                       moveit_visual_tools::MoveItVisualTools &visual_tools) {
    // Move robot arm to initial pose
    geometry_msgs::msg::Pose initial_pose;
    initial_pose.position.x = 0.958998;
    initial_pose.position.y = -0.000002;
    initial_pose.position.z = 1.361805;

    std::vector<geometry_msgs::msg::Pose> waypoints;
    waypoints.push_back(initial_pose);

    moveit_msgs::msg::RobotTrajectory trajectory;
    const double jump_threshold = 0.0;
    const double eef_step = 0.01;
    double fraction = move_group_arm.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
    RCLCPP_INFO(LOGGER, "Moving to initial pose (%.2f%% achieved)", fraction * 100.0);

    move_group_arm.execute(trajectory);
    visual_tools.trigger();  // Update RViz visualization
}


void add_object_box(moveit::planning_interface::PlanningSceneInterface &planning_scene_interface,
                moveit_msgs::msg::CollisionObject &object_to_attach) {

    
    // Create collision object for the robot to avoid

    moveit_msgs::msg::CollisionObject box_object;
    // box_object.header.frame_id = frame_id;
    box_object.id = "box1";
    shape_msgs::msg::SolidPrimitive primitive;

    // Define the size of the box in meters
    primitive.type = primitive.BOX;
    primitive.dimensions.resize(3);
    primitive.dimensions[primitive.BOX_X] = 0.07;
    primitive.dimensions[primitive.BOX_Y] = 0.07;
    primitive.dimensions[primitive.BOX_Z] = 0.07;

    // Define the pose of the box (relative to the frame_id)
    geometry_msgs::msg::Pose box_pose;
    box_pose.orientation.w = 1.0;  // We can leave out the x, y, and z components of the quaternion since they are initialized to 0
    box_pose.position.x = 1.16;
    box_pose.position.y = 0.0;
    box_pose.position.z = 0.035;


    object_to_attach.primitive_poses.push_back(box_pose);
    object_to_attach.header.frame_id = "world";
    object_to_attach.operation = moveit_msgs::msg::CollisionObject::ADD;
    object_to_attach.primitives.push_back(primitive);
    planning_scene_interface.applyCollisionObject(object_to_attach);
    }

    // Shape Cylinder
void add_object_cylinder(moveit::planning_interface::PlanningSceneInterface &planning_scene_interface,
                moveit_msgs::msg::CollisionObject &object_to_attach) {
 
    shape_msgs::msg::SolidPrimitive cylinder_primitive;
    cylinder_primitive.type = shape_msgs::msg::SolidPrimitive::CYLINDER;
    cylinder_primitive.dimensions.resize(2);
    cylinder_primitive.dimensions[shape_msgs::msg::SolidPrimitive::CYLINDER_HEIGHT] = 0.2;
    cylinder_primitive.dimensions[shape_msgs::msg::SolidPrimitive::CYLINDER_RADIUS] = 0.02;

    geometry_msgs::msg::Pose cylinder_pose;
    cylinder_pose.position.x = 1.45;
    cylinder_pose.position.y = 0.0;
    cylinder_pose.position.z = 0.075;
    cylinder_pose.orientation.w = 1.0;


    object_to_attach.primitive_poses.push_back(cylinder_pose);
    object_to_attach.header.frame_id = "world";
    object_to_attach.operation = moveit_msgs::msg::CollisionObject::ADD;
    object_to_attach.primitives.push_back(cylinder_primitive);
    planning_scene_interface.applyCollisionObject(object_to_attach);
}

void approach_to_object_joint_ankle(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                moveit::planning_interface::MoveGroupInterface &move_group_gripper,
                moveit_visual_tools::MoveItVisualTools &visual_tools) {
    // Arm initial pose joint ankle
    std::vector<double> arm_pose_pickup = {0.0, 1.1547, 0.0, 0.0, 0.0, 0.0};
    move_group_arm.setJointValueTarget(arm_pose_pickup);

    moveit::planning_interface::MoveGroupInterface::Plan arm_plan;

     if (move_group_arm.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
        move_group_arm.move();
        RCLCPP_INFO(LOGGER, "Yaskawa ARM in pickup pose.");
    } else {
        RCLCPP_ERROR(LOGGER, "Yaskawa ARM failed to get in pickup pose");
    }

    visual_tools.trigger();  // Update RViz visualization
}


void approach_to_object(moveit::planning_interface::MoveGroupInterface &move_group_arm) {
    // Move arm to a new position
    geometry_msgs::msg::Pose target_pose2;
    target_pose2.position.x = 1.25;
    target_pose2.position.y = 0.0;
    target_pose2.position.z = 0.2;

    std::vector<geometry_msgs::msg::Pose> waypoints;
    waypoints.push_back(target_pose2);

    moveit_msgs::msg::RobotTrajectory trajectory;
    const double jump_threshold = 0.0;
    const double eef_step = 0.01;
    double fraction = move_group_arm.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
    RCLCPP_INFO(LOGGER, "Visualizing Cartesian path (%.2f%% achieved)", fraction * 100.0);

    move_group_arm.execute(trajectory);
}

void grasp_object(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                moveit::planning_interface::MoveGroupInterface &move_group_gripper,
                moveit_msgs::msg::CollisionObject &object_to_attach) {
    // Close the gripper
    std::vector<double> closed_gripper_position = {0.45, -0.45, 0.45, -0.45, 0.45, -0.45};
    move_group_gripper.setJointValueTarget(closed_gripper_position);
    moveit::planning_interface::MoveGroupInterface::Plan gripper_plan;
    if (move_group_gripper.plan(gripper_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
        move_group_gripper.move();
        RCLCPP_INFO(LOGGER, "Gripper closed successfully.");
    } else {
        RCLCPP_ERROR(LOGGER, "Failed to plan the gripper closing motion.");
    }

    // Attach the object to the robot
    std::vector<std::string> touch_links = {"robotiq_85_base_link"};
    move_group_arm.attachObject(object_to_attach.id, "robotiq_85_base_link", touch_links);
     RCLCPP_INFO(LOGGER, "Gripper grasped the object successfully.");
}
void pickup_object_joint_ankle(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                moveit::planning_interface::MoveGroupInterface &move_group_gripper,
                moveit_visual_tools::MoveItVisualTools &visual_tools) {
    // Arm lifting up the object
    std::vector<double> arm_inital_pose = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    move_group_arm.setJointValueTarget(arm_inital_pose);

    moveit::planning_interface::MoveGroupInterface::Plan arm_plan;

     if (move_group_arm.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
        move_group_arm.move();
        RCLCPP_INFO(LOGGER, "The Object is lifted up.");
    } else {
        RCLCPP_ERROR(LOGGER, "Yaskawa ARM failed to lift up the object");
    }

     visual_tools.trigger();  // Update RViz visualization
                }


void pick_up_object(moveit::planning_interface::MoveGroupInterface &move_group_arm) {
    // Lift the object
    geometry_msgs::msg::Pose liftup_pose;
    liftup_pose.position.x = 0.958998;
    liftup_pose.position.y = -0.000002;
    liftup_pose.position.z = 1.361805;

    std::vector<geometry_msgs::msg::Pose> waypoints;
    waypoints.push_back(liftup_pose);

    moveit_msgs::msg::RobotTrajectory trajectory;
    const double jump_threshold = 0.0;
    const double eef_step = 0.001;
    double fraction = move_group_arm.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
    RCLCPP_INFO(LOGGER, "Visualizing Cartesian path (%.2f%% achieved)", fraction * 100.0);
    move_group_arm.execute(trajectory);
}


void place_object_joint_ankle(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                  moveit_visual_tools::MoveItVisualTools &visual_tools,
                  moveit_msgs::msg::CollisionObject &object_to_attach) {
    // Move robot arm to the place pose
    // Arm initial pose joint ankle
    std::vector<double> arm_pose = {1.2016, 1.2041, 0.0, 0.0, 0.0, 0.2836};
    move_group_arm.setJointValueTarget(arm_pose);
    moveit::planning_interface::MoveGroupInterface::Plan arm_plan;

     if (move_group_arm.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
        move_group_arm.move();
        RCLCPP_INFO(LOGGER, "Yaskawa ARM in pose to PLACE.");
    } else {
        RCLCPP_ERROR(LOGGER, "Yaskawa ARM failed to get in place pose");
    
    }

    move_group_arm.detachObject(object_to_attach.id);
    RCLCPP_INFO(LOGGER, "The object is placed");

}

void place_object(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                  moveit_visual_tools::MoveItVisualTools &visual_tools,
                  moveit_msgs::msg::CollisionObject &object_to_attach) {
    // Move robot arm to the place pose
    geometry_msgs::msg::Pose place_pose;
    place_pose.position.x = 0.9;
    place_pose.position.y = 0.35;
    place_pose.position.z = 0.035;

    std::vector<geometry_msgs::msg::Pose> waypoints;
    waypoints.push_back(place_pose);

    moveit_msgs::msg::RobotTrajectory trajectory;
    const double jump_threshold = 0.0;
    const double eef_step = 0.01;
    double fraction = move_group_arm.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
    RCLCPP_INFO(LOGGER, "Moving to place pose (%.2f%% achieved)", fraction * 100.0);

    move_group_arm.execute(trajectory);
    visual_tools.trigger();  // Update RViz visualization

    move_group_arm.detachObject(object_to_attach.id);
    RCLCPP_INFO(LOGGER, "The object is placed");
}

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::NodeOptions node_options;
    node_options.automatically_declare_parameters_from_overrides(true);
    auto move_group_node = rclcpp::Node::make_shared("move_group_interface", node_options);
    
    // Add collision object
    moveit_msgs::msg::CollisionObject object_to_attach;
    object_to_attach.id = "cylinder1";

    
    rclcpp::executors::SingleThreadedExecutor executor;
    executor.add_node(move_group_node);
    std::thread([&executor]() { executor.spin(); }).detach();

    static const std::string PLANNING_GROUP_ARM = "arm";
    static const std::string PLANNING_GROUP_GRIPPER = "gripper";

    moveit::planning_interface::MoveGroupInterface move_group_arm(move_group_node, PLANNING_GROUP_ARM);
    moveit::planning_interface::MoveGroupInterface move_group_gripper(move_group_node, PLANNING_GROUP_GRIPPER);
    moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

    moveit_visual_tools::MoveItVisualTools visual_tools(
    move_group_node,                           // The rclcpp::Node::SharedPtr
    "base_link",                               // The reference frame for the visual tools
    "rviz_visual_tools"                        // Marker topic to publish to RViz
    );

    // moveit_visual_tools::MoveItVisualTools visual_tools("base_link", rclcpp::Node::SharedPtr(), move_group_arm.getRobotModel());

    for (int i = 0; i < 500; ++i) {

        
        // moveToInitialPose_JointAnkle(move_group_arm, move_group_gripper,visual_tools);
        moveToInitialPose(move_group_arm, visual_tools);
        add_object_box(planning_scene_interface, object_to_attach);
        approach_to_object_joint_ankle(move_group_arm, move_group_gripper,visual_tools);
        grasp_object(move_group_arm, move_group_gripper,object_to_attach);
        pickup_object_joint_ankle(move_group_arm, move_group_gripper,visual_tools);      
        place_object_joint_ankle(move_group_arm, visual_tools, object_to_attach);
        moveToInitialPose_JointAnkle(move_group_arm, move_group_gripper,visual_tools);
        
        RCLCPP_INFO(LOGGER, "Iteration is completed %d", i);
        std::this_thread::sleep_for(std::chrono::seconds(5));
    }

    rclcpp::shutdown();
    return 0;
}
