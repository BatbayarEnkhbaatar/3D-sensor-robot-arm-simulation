#include <cstdio>
#include <functional>
#include <memory>
#include <thread>
#include "robotic_msgs/action/robotic_tasks.hpp"
#include <rclcpp_components/register_node_macro.hpp>
#include <rclcpp/rclcpp.hpp>
#include "rclcpp_action/rclcpp_action.hpp"

using namespace std::placeholders;

namespace RoboticTasks
{
class TaskServer : public rclcpp::Node
{
public:
    explicit TaskServer(const rclcpp::NodeOptions &options = rclcpp::NodeOptions()) : Node("task_server", options)
    {
        action_server_ = rclcpp_action::create_server<robotic_msgs::action::RoboticTasks>(
            this, "task_server", std::bind(&TaskServer::goalCallback, this, _1, _2),
            std::bind(&TaskServer::cancelCallback, this, _1),
            std::bind(&TaskServer::acceptCallback, this, _1)
        );
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Starting the Action Server...");
    }

private:
    rclcpp_action::Server<robotic_msgs::action::RoboticTasks>::SharedPtr action_server_;

    rclcpp_action::GoalResponse goalCallback(const rclcpp_action::GoalUUID &uuid, std::shared_ptr<const robotic_msgs::action::RoboticTasks::Goal> goal)
    {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received goal request with id: %d", goal->task_number);
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;    

    }

    rclcpp_action::CancelResponse cancelCallback(const std::shared_ptr<rclcpp_action::ServerGoalHandle<robotic_msgs::action::RoboticTasks>> goal_handle)
    {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received request to cancel the goal");
        // auto arm_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm_group");
        // arm_move_group.stop();
        return rclcpp_action::CancelResponse::ACCEPT;
    }

    void acceptCallback(const std::shared_ptr<rclcpp_action::ServerGoalHandle<robotic_msgs::action::RoboticTasks>> goal_handle)
    {
        std::thread{&TaskServer::execute, this, goal_handle}.detach();
    }

    void execute(const std::shared_ptr<rclcpp_action::ServerGoalHandle<robotic_msgs::action::RoboticTasks>> goal_handle)
    {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Executing goal");

        // auto arm_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm_group");

        // std::vector<double> arm_joint_goal;
        // if (goal_handle->get_goal()->task_number == 0)
        // {
        //     arm_joint_goal = {0.0, -0.5, 0.0, 0.0, 0.0, 0.0};
        // }
        // else if (goal_handle->get_goal()->task_number == 1)
        // {
        //     arm_joint_goal =  {-0.14, 0.5, 0.0, 0.0, 0.0, 0.0};
        // }

        // else if (goal_handle->get_goal()->task_number == 2)
        // {
        //     arm_joint_goal = {0.15, 1.5, 0.0, 0.0, 0.0, 0.0};
        // } %d", goal->
        // else
        // {
        //     RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Invalid task number!!!!");
        //     return;
        // }

        // bool arm_within_bounds = arm_move_group.setJointValueTarget(arm_joint_goal);

        // if (!arm_within_bounds)
        // {
        //     RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Target joint position was outside the limits Please try again");
        // }
 
        // moveit::planning_interface::MoveGroupInterface::Plan arm_plan;
        // bool arm_plan_success = arm_move_group.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS;
        // if (arm_plan_success)
        // {
        //     RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Planner succeeded");
        //     arm_move_group.move();
        // }
        // else
        // {
        //     RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "One or more planners failed");
        // }

        auto result = std::make_shared<robotic_msgs::action::RoboticTasks::Result>();
        result->success = true;
        goal_handle->succeed(result);

        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Goal succeeded");
    }
};
}

RCLCPP_COMPONENTS_REGISTER_NODE(RoboticTasks::TaskServer)
