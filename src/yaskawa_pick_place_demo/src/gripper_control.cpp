#include <chrono>
#include <memory>
#include <string>

#include <rclcpp/rclcpp.hpp>
#include <trajectory_msgs/msg/joint_trajectory.hpp>
#include <trajectory_msgs/msg/joint_trajectory_point.hpp>

using namespace std::chrono_literals;

class GripperTestNode : public rclcpp::Node
{
public:
  GripperTestNode()
  : Node("gripper_test_node")
  {
    // Parameters
    joint_name_ = this->declare_parameter<std::string>("joint_name", "robotiq_85_left_knuckle_joint");
    close_pos_  = this->declare_parameter<double>("close_pos", 0.35);
    open_pos_   = this->declare_parameter<double>("open_pos", 0.0);
    move_time_  = this->declare_parameter<double>("move_time", 0.2); 

    // Publisher
    gripper_pub_ = this->create_publisher<trajectory_msgs::msg::JointTrajectory>(
      "/gripper_controller/joint_trajectory", 10);

    // Timer to alternate open/close
    timer_ = this->create_wall_timer(
      2s, std::bind(&GripperTestNode::toggle_gripper, this));
  }

private:
  void toggle_gripper()
  {
    bool close = toggle_state_;
    toggle_state_ = !toggle_state_;

    double target_pos = close ? close_pos_ : open_pos_;
    std::string action = close ? "Closing" : "Opening";

    RCLCPP_INFO(get_logger(), "%s gripper to position %.3f", action.c_str(), target_pos);

    trajectory_msgs::msg::JointTrajectory traj;
    traj.joint_names.push_back(joint_name_);

    trajectory_msgs::msg::JointTrajectoryPoint point;
    point.positions.push_back(target_pos);
    point.time_from_start = rclcpp::Duration::from_seconds(move_time_);

    traj.points.push_back(point);

    gripper_pub_->publish(traj);
  }

  // Parameters
  std::string joint_name_;
  double close_pos_;
  double open_pos_;
  double move_time_;

  // ROS interfaces
  rclcpp::Publisher<trajectory_msgs::msg::JointTrajectory>::SharedPtr gripper_pub_;
  rclcpp::TimerBase::SharedPtr timer_;

  bool toggle_state_ = true; // start with closing
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<GripperTestNode>());
  rclcpp::shutdown();
  return 0;
}
