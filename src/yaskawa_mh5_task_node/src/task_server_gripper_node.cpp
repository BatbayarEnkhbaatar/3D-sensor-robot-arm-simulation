#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <rclcpp_components/register_node_macro.hpp>

#include <robotic_msgs/action/robotic_gripper_tasks.hpp>
#include <moveit/move_group_interface/move_group_interface.h>

#include <sstream>
#include <thread>
#include <map>

using GripperCommandMsgs     = robotic_msgs::action::RoboticGripperTasks;
using GripperTasksGoalHandle = rclcpp_action::ServerGoalHandle<GripperCommandMsgs>;
using std::placeholders::_1;
using std::placeholders::_2;

namespace RoboticTasks
{

class GripperTaskServer : public rclcpp::Node
{
public:
  explicit GripperTaskServer(const rclcpp::NodeOptions & options = rclcpp::NodeOptions())
  : Node("RoboticTaskServer_gripper_Node", options)
  {
    // Use a unique action name so it doesn't collide with your arm server
    // const std::string action_name = "/gripper_task_server";

    action_server_ = rclcpp_action::create_server<GripperCommandMsgs>(
      this,
      "task_server_gripper",
      std::bind(&GripperTaskServer::goal_callback,     this, _1, _2),
      std::bind(&GripperTaskServer::cancel_callback,   this, _1),
      std::bind(&GripperTaskServer::accepted_callback, this, _1));

    RCLCPP_INFO(get_logger(), "Gripper Action Server ready on...");
  }

private:
  rclcpp_action::Server<GripperCommandMsgs>::SharedPtr action_server_;

  // --- Callbacks ---

  rclcpp_action::GoalResponse goal_callback(
      const rclcpp_action::GoalUUID &,
      std::shared_ptr<const GripperCommandMsgs::Goal> goal)
  {
    log_sequence(goal->gripper_command);
    if (goal->gripper_command.empty()) {
      RCLCPP_ERROR(get_logger(), "Goal rejected: gripper_command is empty (need one value).");
      return rclcpp_action::GoalResponse::REJECT;
    }
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse cancel_callback(
      const std::shared_ptr<GripperTasksGoalHandle> /*goal_handle*/)
  {
    try {
      moveit::planning_interface::MoveGroupInterface gripper(shared_from_this(), "gripper");
      gripper.stop();
      RCLCPP_INFO(get_logger(), "Cancel requested: stopping gripper.");
    } catch (const std::exception &e) {
      RCLCPP_WARN(get_logger(), "Cancel stop warning: %s", e.what());
    }
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  void accepted_callback(const std::shared_ptr<GripperTasksGoalHandle> goal_handle)
  {
    auto keepalive = this->shared_from_this();
    std::thread([this, keepalive, goal_handle] {
      execute_goal(goal_handle);
    }).detach();
  }

  void execute_goal(const std::shared_ptr<GripperTasksGoalHandle> goal_handle)
  {
    RCLCPP_INFO(get_logger(), "Executing gripper goal...");
    auto result = std::make_shared<GripperCommandMsgs::Result>();

    // 1) Construct MoveGroup for your gripper. Ensure SRDF group is actually named "gripper".
    moveit::planning_interface::MoveGroupInterface gripper(shared_from_this(), "gripper");

    
    const auto goal = goal_handle->get_goal();
    const double target_value = goal->gripper_command[0];
    
    moveit::planning_interface::MoveGroupInterface::Plan plan;
    gripper.setJointValueTarget({target_value});

    bool plan_ok = (gripper.plan(plan) == moveit::core::MoveItErrorCode::SUCCESS);
    if (!plan_ok) {
      RCLCPP_ERROR(get_logger(), "Gripper planning failed.");
      goal_handle->abort(result);
      return;
    }

    // 5) Execute
    auto exec_ec = gripper.execute(plan);
    if (exec_ec != moveit::core::MoveItErrorCode::SUCCESS) {
      RCLCPP_ERROR(get_logger(), "Gripper execution failed.");
      goal_handle->abort(result);
      return;
    }

    // Done
    result->success = true;
    goal_handle->succeed(result);
    RCLCPP_INFO(get_logger(), "Gripper goal executed successfully.");
  }

  void log_sequence(const std::vector<double> &seq)
  {
    std::ostringstream oss;
    oss << "[";
    for (size_t i = 0; i < seq.size(); ++i) {
      oss << seq[i];
      if (i + 1 < seq.size()) oss << ", ";
    }
    oss << "]";
    RCLCPP_INFO(get_logger(), "Received GRIPPER COMMAND: %s", oss.str().c_str());
  }
};

}  // namespace RoboticTasks

RCLCPP_COMPONENTS_REGISTER_NODE(RoboticTasks::GripperTaskServer)
