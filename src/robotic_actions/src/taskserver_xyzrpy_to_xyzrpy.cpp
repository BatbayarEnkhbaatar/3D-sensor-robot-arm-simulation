#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <robotic_msgs/action/yaskawa_tasks.hpp>
#include <sstream>
#include <rclcpp_components/register_node_macro.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <geometry_msgs/msg/pose_stamped.hpp>

using RoboticTaskMsgs = robotic_msgs::action::YaskawaTasks;
using RoboticTasksGoalHandle = rclcpp_action::ServerGoalHandle<RoboticTaskMsgs>;
using namespace std::placeholders;

namespace RoboticTasks
{
class RoboticTaskServerRPY : public rclcpp::Node 
{
public: 
    explicit RoboticTaskServerRPY(const rclcpp::NodeOptions &options = rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true)) 
    : Node("RoboticTaskServer_Node", options)
    {
        action_server_ = rclcpp_action::create_server<RoboticTaskMsgs>(
            this,
            "YaskawaTasks",
            std::bind(&RoboticTaskServerRPY::goal_callback, this, _1, _2),
            std::bind(&RoboticTaskServerRPY::cancel_callback, this, _1),
            std::bind(&RoboticTaskServerRPY::accepted_callback, this, _1));
        RCLCPP_INFO(this->get_logger(), "Action Server for XYZRPY is getting started...");
    }

private:
    rclcpp_action::Server<RoboticTaskMsgs>::SharedPtr action_server_;

    rclcpp_action::GoalResponse goal_callback(
        const rclcpp_action::GoalUUID &uuid, std::shared_ptr<const RoboticTaskMsgs::Goal> goal)
    {
        log_task_sequences(goal->task_sequences);
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    }

    rclcpp_action::CancelResponse cancel_callback(
        const std::shared_ptr<RoboticTasksGoalHandle> goal_handle)
    {
        RCLCPP_INFO(this->get_logger(), "Cancelling the current task...");
        // Robot arm trajectory instance
        auto arm_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm");
        arm_group.stop();

        // Robot gripper instance (commented out)
        // auto gripper_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "gripper");
        // gripper_group.stop();

        return rclcpp_action::CancelResponse::ACCEPT;
    }

    void accepted_callback(
        const std::shared_ptr<RoboticTasksGoalHandle> goal_handle)
    {
        std::thread{std::bind(&RoboticTaskServerRPY::execute_goal, this, _1), goal_handle}.detach();
    }

    void execute_goal(const std::shared_ptr<RoboticTasksGoalHandle> goal_handle)
    {
        RCLCPP_INFO(this->get_logger(), "Action Server received the command and executing...");
        auto goal = goal_handle->get_goal();

        // Robot arm trajectory instance
        auto arm_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm");
                // Retrieve the current pose of the robot's end-effector
        geometry_msgs::msg::PoseStamped current_pose = arm_group.getCurrentPose();
        
        RCLCPP_INFO(this->get_logger(), "Current Pose:");
        RCLCPP_INFO(this->get_logger(), "Position: [X: %f, Y: %f, Z: %f]", 
                    current_pose.pose.position.x, 
                    current_pose.pose.position.y, 
                    current_pose.pose.position.z);
                    
        RCLCPP_INFO(this->get_logger(), "Orientation: [X: %f, Y: %f, Z: %f, W: %f]", 
                    current_pose.pose.orientation.x, 
                    current_pose.pose.orientation.y, 
                    current_pose.pose.orientation.z, 
                    current_pose.pose.orientation.w);

                    
        // Create a pose object with the desired end-effector position and orientation
        geometry_msgs::msg::PoseStamped target_pose;
        auto desired_pose = goal->task_sequences;
        target_pose.header.frame_id = "base_link";
        target_pose.pose.position.x = desired_pose[0];
        target_pose.pose.position.y = desired_pose[1];
        target_pose.pose.position.z = desired_pose[2];



        // tf2::Quaternion quaternion;
        // auto roll = desired_pose[3];
        // auto pitch = desired_pose[4];
        // auto yaw = desired_pose[5];
        // quaternion.setRPY(roll, pitch, yaw);

        RCLCPP_INFO(this->get_logger(), "XYZ and RPY are converted successfully");
        RCLCPP_INFO(this->get_logger(), "Goal Pose: ");
        RCLCPP_INFO(this->get_logger(), "Goal Pose X, Y, Z: %f, %f, %f", target_pose.pose.position.x, target_pose.pose.position.y, target_pose.pose.position.z);
        RCLCPP_INFO(this->get_logger(), "Goal Orientation Roll, Pitch, Yaw, W: %f, %f, %f", 
                    desired_pose[3], desired_pose[4], desired_pose[5]);
        // Extract quaternion components
        // double x = desired_pose[3];
        // double y = desired_pose[4];
        // double z = desired_pose[5];
   

        // Print quaternion components
        // RCLCPP_INFO(this->get_logger(), "Quaternion components converted:");
        // RCLCPP_INFO(this->get_logger(), "x: %f", x);
        // RCLCPP_INFO(this->get_logger(), "y: %f", y);
        // RCLCPP_INFO(this->get_logger(), "z: %f", z);
        // RCLCPP_INFO(this->get_logger(), "w: %f", w);
        RCLCPP_INFO(this->get_logger(), "Setting target pose for the end-effector...");
        

        target_pose.pose.orientation.x = desired_pose[3];
        target_pose.pose.orientation.y = desired_pose[4];
        target_pose.pose.orientation.z = desired_pose[5];
        target_pose.pose.orientation.w = desired_pose[6];

        RCLCPP_INFO(this->get_logger(), "Applied target pose to End-Effector:");
        RCLCPP_INFO(this->get_logger(), "x: %f", target_pose.pose.orientation.x);
        RCLCPP_INFO(this->get_logger(), "y: %f",target_pose.pose.orientation.y);
        RCLCPP_INFO(this->get_logger(), "z: %f", target_pose.pose.orientation.z);
        RCLCPP_INFO(this->get_logger(), "w: %f", target_pose.pose.orientation.w);
        RCLCPP_INFO(this->get_logger(), "Setting target pose for the end-effector...");
        
        arm_group.setPoseTarget(target_pose, "robotiq_85_base_link");
 
        arm_group.setPlanningTime(4.0);
        arm_group.setMaxVelocityScalingFactor(0.10);

        arm_group.setNumPlanningAttempts(3); 
        arm_group.setGoalTolerance(0.5);
        moveit::planning_interface::MoveGroupInterface::Plan arm_plan;
                // Convert RPY (Roll, Pitch, Yaw) to a quaternion
        RCLCPP_INFO(this->get_logger(), "Reference Frame: '%s'", arm_group.getPlanningFrame().c_str());
        RCLCPP_INFO(this->get_logger(), "End-Effector: '%s'", arm_group.getEndEffectorLink().c_str());
        RCLCPP_INFO(this->get_logger(), "Planning the motion...");

        if (arm_group.plan(arm_plan) != moveit::core::MoveItErrorCode::SUCCESS) {
            RCLCPP_ERROR(this->get_logger(), "Failed to plan the arm motion.");
            goal_handle->abort(std::make_shared<RoboticTaskMsgs::Result>());
            return;
        }
        else {
            RCLCPP_ERROR(this->get_logger(), "Motion Planning is sent...");
        }

        RCLCPP_INFO(this->get_logger(), "Executing planned motion...");
        if (arm_group.move() != moveit::core::MoveItErrorCode::SUCCESS) {
            RCLCPP_ERROR(this->get_logger(), "Failed to execute the planned motion.");
            goal_handle->abort(std::make_shared<RoboticTaskMsgs::Result>());
            return;
        }

        auto result = std::make_shared<RoboticTaskMsgs::Result>();
        result->success = true;
        goal_handle->succeed(result);
        RCLCPP_INFO(this->get_logger(), "Goal achieved successfully.");



    }

    void log_task_sequences(const std::vector<double> &task_sequences)
    {
        std::ostringstream oss;
        oss << "[";
        for (size_t i = 0; i < task_sequences.size(); ++i) {
            oss << task_sequences[i];
            if (i < task_sequences.size() - 1) {
                oss << ", ";
            }
        }
        oss << "]";
        RCLCPP_INFO(this->get_logger(), "Received goal request with task sequences: %s", oss.str().c_str());
    }
};

} // namespace RoboticTasks

// RCLCPP_COMPONENTS_REGISTER_NODE(RoboticTasks::RoboticTaskServerRPY)

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<RoboticTasks::RoboticTaskServerRPY>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
