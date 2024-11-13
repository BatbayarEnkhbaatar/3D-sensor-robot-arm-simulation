#include <functional>
#include <memory>
#include <thread>

#include "robotic_msgs/action/yaskawa_tasks.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "rclcpp_components/register_node_macro.hpp"
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

using namespace std::placeholders;

namespace yaskawa_remote
{
class TaskServer : public rclcpp::Node
{
public: 
      int place_where = 0;
    explicit TaskServer(const rclcpp::NodeOptions &options = rclcpp::NodeOptions()) : Node("task_server", options) {
        action_server_ = rclcpp_action::create_server<robotic_msgs::action::YaskawaTasks>(
            this, "task_server",
            std::bind(&TaskServer::goalCallback, this, _1, _2),
            std::bind(&TaskServer::cancelCallback, this, _1),
            std::bind(&TaskServer::acceptCallback, this, _1)
        );

        // Create collision object for the robot to avoid
        auto planning_scene_interface = moveit::planning_interface::PlanningSceneInterface();

        moveit_msgs::msg::CollisionObject box_object;

        box_object.id = "box1";
        box_object.header.frame_id = "world";

        shape_msgs::msg::SolidPrimitive primitive;
        primitive.type = primitive.BOX;
        primitive.dimensions.resize(3);
        primitive.dimensions[primitive.BOX_X] = 0.07;
        primitive.dimensions[primitive.BOX_Y] = 0.07;
        primitive.dimensions[primitive.BOX_Z] = 0.07;

        geometry_msgs::msg::Pose box_pose;
        box_pose.orientation.w = 1.0;
        box_pose.position.x = 1.16;
        box_pose.position.y = 0.0;
        box_pose.position.z = 0.035;

        box_object.primitives.push_back(primitive);
        box_object.primitive_poses.push_back(box_pose);
        box_object.operation = moveit_msgs::msg::CollisionObject::ADD;

        planning_scene_interface.applyCollisionObject(box_object);

        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Starting the Action Server");
    }

private:
    rclcpp_action::Server<robotic_msgs::action::YaskawaTasks>::SharedPtr action_server_;

    rclcpp_action::GoalResponse goalCallback(
        const rclcpp_action::GoalUUID &uuid, 
        std::shared_ptr<const robotic_msgs::action::YaskawaTasks::Goal> goal) 
    {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received goal request with task number: %d", goal->task_number);
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    }

    rclcpp_action::CancelResponse cancelCallback(
        const std::shared_ptr<rclcpp_action::ServerGoalHandle<robotic_msgs::action::YaskawaTasks>> goal_handle) 
    {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received request to cancel the goal");

        auto arm_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm_group");
        arm_move_group.stop();

        return rclcpp_action::CancelResponse::ACCEPT;
    }

    void acceptCallback(
        const std::shared_ptr<rclcpp_action::ServerGoalHandle<robotic_msgs::action::YaskawaTasks>> goal_handle) 
    {
        std::thread{&TaskServer::execute, this, goal_handle}.detach();
    }

    void execute(const std::shared_ptr<rclcpp_action::ServerGoalHandle<robotic_msgs::action::YaskawaTasks>> goal_handle)
    {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Executing goal");
        moveit_msgs::msg::CollisionObject object_to_attach;
        object_to_attach.id = "box1";
        
        auto arm_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm");
        auto gripper_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "gripper");  // Correct group name for the gripper

        auto goal = goal_handle->get_goal();
        double task_number = goal->task_number;

        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received command is that:  %.2f", task_number);
        if (place_where ==0) {
            if (task_number ==1.0){
                moveToInitialPose_JointAnkle(arm_move_group, gripper_move_group);
                approach_to_object_joint_ankle(arm_move_group, gripper_move_group);
                moveToInitialPose_JointAnkle(arm_move_group, gripper_move_group);
                RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received command is %.2f", task_number);
            }

            if (task_number == 2.0)
            {     
                RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received command is %.2f", task_number);
                
                    approach_to_object_joint_ankle(arm_move_group, gripper_move_group);
                    grasp_object(arm_move_group, gripper_move_group, object_to_attach );
                    pickup_object_joint_ankle(arm_move_group, gripper_move_group);
            }
                if (task_number == 3.0)
            {     
                RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received command is %.2f", task_number);
                // approach_to_object_joint_ankle(arm_move_group, gripper_move_group);
                // grasp_object(arm_move_group, gripper_move_group, object_to_attach );
                // pickup_object_joint_ankle(arm_move_group, gripper_move_group);
                place_object_joint_ankle(arm_move_group );
                detach_object(arm_move_group, object_to_attach, 1);
                moveToInitialPose_JointAnkle(arm_move_group, gripper_move_group);
            }
        }
        if (place_where ==1) {
            if (task_number ==1.0){
                moveToInitialPose_JointAnkle(arm_move_group, gripper_move_group);
                approach_to_object_joint_ankle(arm_move_group, gripper_move_group);
                moveToInitialPose_JointAnkle(arm_move_group, gripper_move_group);
                RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received command is %.2f", task_number);
            }

            if (task_number == 2.0)
            {     
                RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received command is %.2f", task_number);
                
                    place_object_joint_ankle(arm_move_group);
                    grasp_object(arm_move_group, gripper_move_group, object_to_attach );
                    pickup_object_joint_ankle(arm_move_group, gripper_move_group);
            }
                if (task_number == 3.0)
            {     
                RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received command is %.2f", task_number);
                // approach_to_object_joint_ankle(arm_move_group, gripper_move_group);
                // grasp_object(arm_move_group, gripper_move_group, object_to_attach );
                // pickup_object_joint_ankle(arm_move_group, gripper_move_group);
                place_object_joint_ankle(arm_move_group );
                grasp_object(arm_move_group, gripper_move_group, object_to_attach);
                moveToInitialPose_JointAnkle(arm_move_group, gripper_move_group);
                approach_to_object_joint_ankle(arm_move_group, gripper_move_group);
                detach_object(arm_move_group, object_to_attach, 0);
                moveToInitialPose_JointAnkle(arm_move_group, gripper_move_group);
                
            }
        }
        }

    //########################################
    // Placing the object
    //########################################
    
    void place_object_joint_ankle(moveit::planning_interface::MoveGroupInterface &move_group_arm) {
    // Move robot arm to the place pose
    // Arm initial pose joint ankle
    std::vector<double> arm_pose = {1.2016, 1.2041, 0.0, 0.0, 0.0, 0.2836};
    move_group_arm.setJointValueTarget(arm_pose);
    moveit::planning_interface::MoveGroupInterface::Plan arm_plan;

     if (move_group_arm.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
        move_group_arm.move();
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Yaskawa ARM in pose to PLACE.");
    } else {
        RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Yaskawa ARM failed to get in place pose");
    
    }

    
    }

    void detach_object(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                  moveit_msgs::msg::CollisionObject &object_to_attach, int last_loc) { 
        move_group_arm.detachObject(object_to_attach.id);
        place_where = last_loc;
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "The object is placed");
        }

    //########################################
    // grasping the object
    //########################################
    
    void grasp_object(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                moveit::planning_interface::MoveGroupInterface &move_group_gripper,
                 moveit_msgs::msg::CollisionObject &object_to_attach) {
       
        std::vector<double> closed_gripper_position = {0.45, -0.45, 0.45, -0.45, 0.45, -0.45};
        move_group_gripper.setJointValueTarget(closed_gripper_position);
        
        moveit::planning_interface::MoveGroupInterface::Plan gripper_plan;
        if (move_group_gripper.plan(gripper_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
            move_group_gripper.move();
            // Attach the object to the robot
            std::vector<std::string> touch_links = {"robotiq_85_base_link"};
            move_group_arm.attachObject(object_to_attach.id, "robotiq_85_base_link", touch_links);
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Gripper grasped the object successfully.");
        } else {
            RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to plan the gripper closing motion.");
        }

        
    }
    
    //########################################
    //Pick up the object 
    //########################################
    
    void pickup_object_joint_ankle(moveit::planning_interface::MoveGroupInterface &move_group_arm,
                moveit::planning_interface::MoveGroupInterface &move_group_gripper) {
        //########################################
        // Arm lifting up the object
        //########################################
        std::vector<double> arm_inital_pose = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
        move_group_arm.setJointValueTarget(arm_inital_pose);

        moveit::planning_interface::MoveGroupInterface::Plan arm_plan;

        if (move_group_arm.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
            move_group_arm.move();
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "The Object is lifted up.");
        } else {
            RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Yaskawa ARM failed to lift up the object");
        }
    }

    void moveToInitialPose_JointAnkle(
        moveit::planning_interface::MoveGroupInterface &move_group_arm,
        moveit::planning_interface::MoveGroupInterface &move_group_gripper) 
    {
        std::vector<double> arm_inital_pose = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
        move_group_arm.setJointValueTarget(arm_inital_pose);

        moveit::planning_interface::MoveGroupInterface::Plan arm_plan;

        if (move_group_arm.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
            move_group_arm.move();
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Yaskawa ARM in initial pose.");
        } else {
            RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Yaskawa ARM failed to get in initial pose.");
        }

        std::vector<double> openned_gripper_position = {0.2, -0.2, 0.2, -0.2, 0.2, -0.2};
        move_group_gripper.setJointValueTarget(openned_gripper_position);

        moveit::planning_interface::MoveGroupInterface::Plan gripper_plan;
        if (move_group_gripper.plan(gripper_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
            move_group_gripper.move();
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Gripper opened successfully.");
        } else {
            RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to plan the gripper opening motion.");
        }
    }

    void approach_to_object_joint_ankle(
        moveit::planning_interface::MoveGroupInterface &move_group_arm,
        moveit::planning_interface::MoveGroupInterface &move_group_gripper) 
    {
        std::vector<double> arm_pose_pickup = {0.0, 1.157, 0.0, 0.0, 0.0, 0.0};
        move_group_arm.setJointValueTarget(arm_pose_pickup);

        moveit::planning_interface::MoveGroupInterface::Plan arm_plan;

        if (move_group_arm.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS) {
            move_group_arm.move();
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Yaskawa ARM in pickup pose.");
        } else {
            RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Yaskawa ARM failed to get in pickup pose.");
        }
    }

};

}  // namespace yaskawa_remote

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<yaskawa_remote::TaskServer>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
