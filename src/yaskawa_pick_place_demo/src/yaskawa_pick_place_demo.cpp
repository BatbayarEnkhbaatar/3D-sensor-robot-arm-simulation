// file: src/pick_place_demo_node.cpp

#include <memory>
#include <string>
#include <chrono>
#include <functional>

#include <rclcpp/rclcpp.hpp>

// MoveIt
#include <moveit/move_group_interface/move_group_interface.h>

// LinkAttacher services
#include <linkattacher_msgs/srv/attach_link.hpp>
#include <linkattacher_msgs/srv/detach_link.hpp>

// Gripper: publish directly to the JointTrajectoryController
#include <trajectory_msgs/msg/joint_trajectory.hpp>
#include <trajectory_msgs/msg/joint_trajectory_point.hpp>

using namespace std::chrono_literals;

class PickPlaceDemo : public rclcpp::Node
{
public:
  PickPlaceDemo()
  : rclcpp::Node("pick_place_demo")
  {
    // ---- Parameters ----
    arm_group_  = this->declare_parameter<std::string>("arm_group", "arm");

    approach_   = this->declare_parameter<std::string>("approach_state", "pickup");
    lift_       = this->declare_parameter<std::string>("lift_state",     "lift_up");
    place_      = this->declare_parameter<std::string>("place_state",    "release");
    home_       = this->declare_parameter<std::string>("home_state",     "home");

    // Gripper publishing settings
    joint_name_ = this->declare_parameter<std::string>("joint_name", "robotiq_85_left_knuckle_joint");
    close_pos_  = this->declare_parameter<double>("close_pos", 0.40);
    open_pos_   = this->declare_parameter<double>("open_pos",  0.00);
    move_time_  = this->declare_parameter<double>("move_time", 0.20); // seconds

    // IFRA LinkAttacher names (adjust if different)
    model1_name_ = this->declare_parameter<std::string>("model1_name", "yaskawa_mh5lf");
    link1_name_  = this->declare_parameter<std::string>("link1_name",  "robotiq_85_base_link");
    model2_name_ = this->declare_parameter<std::string>("model2_name", "dynamic_object");
    link2_name_  = this->declare_parameter<std::string>("link2_name",  "unit_box_link");

    // ---- Interfaces ----
    gripper_pub_ = this->create_publisher<trajectory_msgs::msg::JointTrajectory>(
        "/gripper_controller/joint_trajectory", 10);

    attach_cli_ = this->create_client<linkattacher_msgs::srv::AttachLink>("/ATTACHLINK");
    detach_cli_ = this->create_client<linkattacher_msgs::srv::DetachLink>("/DETACHLINK");

    // Defer MoveGroupInterface until shared_ptr is ready
    init_timer_ = this->create_wall_timer(
      150ms, std::bind(&PickPlaceDemo::deferred_init, this));
  }

private:
  // ========== Lifecycle ==========
  void deferred_init()
  {
    init_timer_->cancel();

    // Now it's safe to pass shared_from_this()
    arm_mgi_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
        this->shared_from_this(), arm_group_);

    // Kick off the sequence shortly after MoveIt connects
    start_timer_ = this->create_wall_timer(
        250ms, std::bind(&PickPlaceDemo::start_sequence, this));
  }

  // ========== Top-level sequence (async chain) ==========
  void start_sequence()
  {
    start_timer_->cancel();

    // 1) Move to approach/grasp pose
    if (!planAndExecuteNamed(approach_)) {
      RCLCPP_ERROR(get_logger(), "Failed to reach approach state: %s", approach_.c_str());
      return;
    }

    // 2) Close gripper quickly
    gripper_move_to(/*close=*/true);
    RCLCPP_INFO(get_logger(), "Gripper close command sent.");

    // 3) Slight delay to let contact settle, then ATTACH asynchronously
    post_attach_timer_ = this->create_wall_timer(
      150ms,
      [this]()
      {
        post_attach_timer_->cancel();
        call_attach_async([this](bool ok){
          if (!ok) {
            RCLCPP_ERROR(this->get_logger(), "Attach failed – aborting sequence");
            return;
          }

          // 4) LIFT named pose
          if (!planAndExecuteNamed(this->lift_)) {
            RCLCPP_ERROR(this->get_logger(), "Lift failed: %s", this->lift_.c_str());
            return;
          }

          // 5) PLACE named pose (optional)
          if (!planAndExecuteNamed(this->place_)) {
            RCLCPP_ERROR(this->get_logger(), "Place move failed: %s", this->place_.c_str());
            // continue anyway to open/detach
          }

          // 6) OPEN gripper quickly
          this->gripper_move_to(/*close=*/false);
          RCLCPP_INFO(this->get_logger(), "Gripper open command sent.");

          // 7) Slight delay, then DETACH asynchronously
          post_detach_timer_ = this->create_wall_timer(
            150ms,
            [this]()
            {
              post_detach_timer_->cancel();
              call_detach_async([this](bool ok){
                if (!ok) {
                  RCLCPP_ERROR(this->get_logger(), "Detach failed");
                  // still try to go home
                }

                // 8) HOME
                if (!planAndExecuteNamed(this->home_)) {
                  RCLCPP_ERROR(this->get_logger(), "Failed to reach home: %s", this->home_.c_str());
                } else {
                  RCLCPP_INFO(this->get_logger(), "Pick–Place sequence complete.");
                }
              });
            });
        });
      });
  }

  // ========== MoveIt helper ==========
  bool planAndExecuteNamed(const std::string& state_name)
  {
    if (!arm_mgi_) {
      RCLCPP_ERROR(get_logger(), "MoveGroupInterface not initialized");
      return false;
    }
    RCLCPP_INFO(get_logger(), "Planning to named target: %s", state_name.c_str());
    arm_mgi_->setStartStateToCurrentState();
    arm_mgi_->setNamedTarget(state_name);

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    if (arm_mgi_->plan(plan) != moveit::planning_interface::MoveItErrorCode::SUCCESS) {
      RCLCPP_ERROR(get_logger(), "Planning failed: %s", state_name.c_str());
      return false;
    }
    if (arm_mgi_->execute(plan) != moveit::planning_interface::MoveItErrorCode::SUCCESS) {
      RCLCPP_ERROR(get_logger(), "Execution failed: %s", state_name.c_str());
      return false;
    }
    RCLCPP_INFO(get_logger(), "Reached: %s", state_name.c_str());
    return true;
  }

  // ========== Gripper (trajectory publisher) ==========
  void gripper_move_to(bool close)
  {
    const double target_pos = close ? close_pos_ : open_pos_;
    const char* action = close ? "Closing" : "Opening";
    RCLCPP_INFO(get_logger(), "%s gripper to %.3f (%.2fs)", action, target_pos, move_time_);

    trajectory_msgs::msg::JointTrajectory traj;
    traj.joint_names.push_back(joint_name_);

    trajectory_msgs::msg::JointTrajectoryPoint pt;
    pt.positions.push_back(target_pos);

    // time_from_start — super fast motion
    pt.time_from_start = rclcpp::Duration::from_seconds(move_time_);
    traj.points.push_back(pt);

    gripper_pub_->publish(traj);
  }

  // ========== LinkAttacher (async, non-blocking) ==========
  void call_attach_async(std::function<void(bool)> on_done)
  {
    if (!attach_cli_->wait_for_service(3s)) {
      RCLCPP_ERROR(get_logger(), "Service /ATTACHLINK not available");
      on_done(false);
      return;
    }

    auto req = std::make_shared<linkattacher_msgs::srv::AttachLink::Request>();
    req->model1_name = model1_name_;
    req->link1_name  = link1_name_;
    req->model2_name = model2_name_;
    req->link2_name  = link2_name_;

    RCLCPP_INFO(get_logger(), "ATTACH: {%s,%s} <-> {%s,%s}",
                model1_name_.c_str(), link1_name_.c_str(),
                model2_name_.c_str(), link2_name_.c_str());

    attach_cli_->async_send_request(
      req,
      [this, on_done](rclcpp::Client<linkattacher_msgs::srv::AttachLink>::SharedFuture fut)
      {
        bool ok = false;
        try {
          const auto& res = fut.get();
          // IFRA_LinkAttacher exposes 'success'
          ok = res->success;
        } catch (const std::exception& e) {
          RCLCPP_ERROR(this->get_logger(), "Attach exception: %s", e.what());
        }
        RCLCPP_INFO(this->get_logger(), "Attach result: %s", ok ? "SUCCESS" : "FAILED");
        on_done(ok);
      });
  }

  void call_detach_async(std::function<void(bool)> on_done)
  {
    if (!detach_cli_->wait_for_service(3s)) {
      RCLCPP_ERROR(get_logger(), "Service /DETACHLINK not available");
      on_done(false);
      return;
    }

    auto req = std::make_shared<linkattacher_msgs::srv::DetachLink::Request>();
    req->model1_name = model1_name_;
    req->link1_name  = link1_name_;
    req->model2_name = model2_name_;
    req->link2_name  = link2_name_;

    RCLCPP_INFO(get_logger(), "DETACH: {%s,%s} <-> {%s,%s}",
                model1_name_.c_str(), link1_name_.c_str(),
                model2_name_.c_str(), link2_name_.c_str());

    detach_cli_->async_send_request(
      req,
      [this, on_done](rclcpp::Client<linkattacher_msgs::srv::DetachLink>::SharedFuture fut)
      {
        bool ok = false;
        try {
          const auto& res = fut.get();
          ok = res->success;
        } catch (const std::exception& e) {
          RCLCPP_ERROR(this->get_logger(), "Detach exception: %s", e.what());
        }
        RCLCPP_INFO(this->get_logger(), "Detach result: %s", ok ? "SUCCESS" : "FAILED");
        on_done(ok);
      });
  }

private:
  // ---- Parameters ----
  std::string arm_group_;
  std::string approach_, lift_, place_, home_;

  // Gripper params
  std::string joint_name_;
  double close_pos_;
  double open_pos_;
  double move_time_;

  // IFRA LinkAttacher names
  std::string model1_name_, link1_name_, model2_name_, link2_name_;

  // ---- Interfaces ----
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> arm_mgi_;
  rclcpp::Publisher<trajectory_msgs::msg::JointTrajectory>::SharedPtr gripper_pub_;
  rclcpp::Client<linkattacher_msgs::srv::AttachLink>::SharedPtr attach_cli_;
  rclcpp::Client<linkattacher_msgs::srv::DetachLink>::SharedPtr detach_cli_;

  // ---- Timers (to chain steps) ----
  rclcpp::TimerBase::SharedPtr init_timer_;
  rclcpp::TimerBase::SharedPtr start_timer_;
  rclcpp::TimerBase::SharedPtr post_attach_timer_;
  rclcpp::TimerBase::SharedPtr post_detach_timer_;
};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<PickPlaceDemo>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
