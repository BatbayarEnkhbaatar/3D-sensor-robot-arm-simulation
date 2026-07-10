#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <robotic_msgs/action/robotic_tasks.hpp>
#include <sstream>
#include <rclcpp_components/register_node_macro.hpp>
#include <moveit/move_group_interface/move_group_interface.h>

#include <geometry_msgs/msg/pose_stamped.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <geometry_msgs/msg/pose.hpp>
#include <geometry_msgs/msg/quaternion.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp> 



using RoboticTaskMsgs = robotic_msgs::action::RoboticTasks;
using RoboticTasksGoalHandle = rclcpp_action::ServerGoalHandle<RoboticTaskMsgs>;
using namespace std::placeholders;

namespace RoboticTasks
{
class RoboticTaskServer : public rclcpp::Node 
{
public: 
    explicit RoboticTaskServer(const rclcpp::NodeOptions &options = rclcpp::NodeOptions()) 
    : Node("RoboticTaskServer_arm_Node", options)
    {
        action_server_ = rclcpp_action::create_server<RoboticTaskMsgs>(
            this,
            "task_server_arm",
            std::bind(&RoboticTaskServer::goal_callback, this, _1, _2),
            std::bind(&RoboticTaskServer::cancel_callback, this, _1),
            std::bind(&RoboticTaskServer::accepted_callback, this, _1));
        RCLCPP_INFO(this->get_logger(), "Arm Action Server ready on... ...");
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
        RCLCPP_INFO(this->get_logger(), "Action Server is getting the new command from...");
        // Robot arm trajectory instance
        auto arm_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm");
        arm_group.stop();

        return rclcpp_action::CancelResponse::ACCEPT;
    }

    void accepted_callback(
        const std::shared_ptr<RoboticTasksGoalHandle> goal_handle)
    {
        std::thread{std::bind(&RoboticTaskServer::execute_goal, this, _1), goal_handle}.detach();
    }

    void execute_goal(const std::shared_ptr<RoboticTasksGoalHandle> goal_handle)
    {
        RCLCPP_INFO(this->get_logger(), "Action Server received the command and executing...");
        auto goal = goal_handle->get_goal();

        // Robot arm trajectory instance
        auto arm_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm");

        arm_group.setPlanningTime(5.0);
        arm_group.setGoalPositionTolerance(0.1);
        arm_group.setGoalOrientationTolerance(0.1);
        arm_group.setMaxVelocityScalingFactor(1.0);
        arm_group.setMaxAccelerationScalingFactor(1.0);
        arm_group.setNumPlanningAttempts(10);
        geometry_msgs::msg::Pose target_pose;
        target_pose.position.x = goal->task_sequences[0];
        target_pose.position.y = goal->task_sequences[1];
        target_pose.position.z = goal->task_sequences[2];

        tf2::Quaternion q;
        q.setRPY(goal->task_sequences[3],
                goal->task_sequences[4],
                goal->task_sequences[5]);
        target_pose.orientation = tf2::toMsg(q);

        bool within_bounds = arm_group.setPoseTarget(target_pose, "link_t");
        if (!within_bounds) {
            RCLCPP_ERROR(get_logger(), "Target pose is out of bounds");
            return;
        }

        moveit::planning_interface::MoveGroupInterface::Plan arm_plan;


        bool arm_plan_success = (arm_group.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS);
        if (arm_plan_success){
            RCLCPP_INFO(this->get_logger(), "Target joint position is reached successfully");
            arm_group.move();
        }
        else
        {
            RCLCPP_ERROR(this->get_logger(), "Oh no, something went wrong...");
            return;
        }

        auto result = std::make_shared<RoboticTaskMsgs::Result>();
        result->success = true;
        goal_handle->succeed(result);
        RCLCPP_INFO(this->get_logger(), "Goal was achieved successfully");
    }     // Choose group via param




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

} 

RCLCPP_COMPONENTS_REGISTER_NODE(RoboticTasks::RoboticTaskServer)
