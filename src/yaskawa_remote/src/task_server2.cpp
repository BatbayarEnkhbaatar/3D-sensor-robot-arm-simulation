#include <functional>
#include <memory>
#include <thread>

#include "yaskawa_msgs/action/yaskawa_tasks.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include <moveit/move_group_interface/move_group_interface.h>

using namespace std::placeholders;

namespace yaskawa_remote
{
class TaskServer : public rclcpp::Node
{
public:
    explicit TaskServer(const rclcpp::NodeOptions &options = rclcpp::NodeOptions()) : Node("task_server", options)
    {
        action_server_ = rclcpp_action::create_server<yaskawa_msgs::action::YaskawaTasks>(
            this, "task_server", std::bind(&TaskServer::goalCallback, this, _1, _2),
            std::bind(&TaskServer::cancelCallback, this, _1),
            std::bind(&TaskServer::acceptCallback, this, _1)
        );
        RCLCPP_INFO(get_logger(), "Starting the Action Server");
    }

private:
    rclcpp_action::Server<yaskawa_msgs::action::YaskawaTasks>::SharedPtr action_server_;

    rclcpp_action::GoalResponse goalCallback(const rclcpp_action::GoalUUID &uuid, std::shared_ptr<const yaskawa_msgs::action::YaskawaTasks::Goal> goal)
    {
        RCLCPP_INFO(get_logger(), "Received goal request with task number: %d", goal->task_number);
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    }

    rclcpp_action::CancelResponse cancelCallback(const std::shared_ptr<rclcpp_action::ServerGoalHandle<yaskawa_msgs::action::YaskawaTasks>> goal_handle)
    {
        RCLCPP_INFO(get_logger(), "Received request to cancel the goal");
        arm_move_group_->stop();
        return rclcpp_action::CancelResponse::ACCEPT;
    }

    void acceptCallback(const std::shared_ptr<rclcpp_action::ServerGoalHandle<yaskawa_msgs::action::YaskawaTasks>> goal_handle)
    {
        std::thread{&TaskServer::execute, this, goal_handle}.detach();
    }

    void execute(const std::shared_ptr<rclcpp_action::ServerGoalHandle<yaskawa_msgs::action::YaskawaTasks>> goal_handle)
    {
        RCLCPP_INFO(get_logger(), "Executing goal");

        arm_move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>("arm_group");
        
        std::vector<std::string> group_state_names = {"start", "sleep"};
        std::vector<std::vector<double>> group_state_values = {{0.0, -0.5, 0.0, 0.0, 0.0, 0.0}, {-0.14, 0.5, 0.0, 0.0, 0.0, 0.0}};
        
        if (goal_handle->get_goal()->task_number >= group_state_names.size()) {
            RCLCPP_ERROR(get_logger(), "Invalid task number");
            return;
        }
        
        // Set the named target based on the task number
        bool success = arm_move_group_->setNamedTarget(group_state_names[goal_handle->get_goal()->task_number]);
        
        if (!success) {
            RCLCPP_ERROR(get_logger(), "Failed to set named target");
            return;
        }
        
        // Plan the motion
        moveit::planning_interface::MoveItErrorCode planning_result = arm_move_group_->plan(arm_plan);
        
        if (planning_result != moveit::planning_interface::MoveItErrorCode::SUCCESS) {
            RCLCPP_ERROR(get_logger(), "Failed to plan motion");
            return;
        }
        
        // Execute the motion
        moveit::planning_interface::MoveItErrorCode execution_result = arm_move_group_->execute(arm_plan);
        
        if (execution_result == moveit::planning_interface::MoveItErrorCode::SUCCESS) {
            RCLCPP_INFO(get_logger(), "Goal succeeded");
            goal_handle->succeed(std::make_shared<yaskawa_msgs::action::YaskawaTasks::Result>());
        } else {
            RCLCPP_ERROR(get_logger(), "Failed to execute motion");
            goal_handle->abort();
        }
    }

    std::shared_ptr
    <moveit::planning_interface::MoveGroupInterface> arm_move_group_;
};
} // namespace yaskawa_remote

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<yaskawa_remote::TaskServer>());
    rclcpp::shutdown();
    return 0;
}
