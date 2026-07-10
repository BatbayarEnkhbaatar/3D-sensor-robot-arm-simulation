#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <sensor_msgs/msg/joint_state.hpp>

#include <fstream>
#include <sstream>
#include <iomanip>
#include <chrono>
#include <mutex>
#include <algorithm>

class EefPoseAndGripperLogger : public rclcpp::Node
{
public:
  EefPoseAndGripperLogger()
  : rclcpp::Node("eef_pose_and_gripper_to_json")
  {
    // ------------ Parameters ------------
    group_              = declare_parameter<std::string>("group_name", "arm");
    file_path_          = declare_parameter<std::string>("file_path", "/tmp/eef_pose.jsonl");
    double rate_hz_in   = declare_parameter<double>("rate_hz", 5.0);
    gripper_joint_name_ = declare_parameter<std::string>("gripper_joint", "robotiq_85_left_knuckle_joint");

    rate_hz_ = std::clamp(rate_hz_in, 1e-3, 200.0);
    period_  = std::chrono::duration_cast<std::chrono::milliseconds>(
                 std::chrono::duration<double>(1.0 / rate_hz_));

    // Open file
    ofs_.open(file_path_, std::ios::out | std::ios::app);
    if (!ofs_) {
      RCLCPP_FATAL(get_logger(), "Failed to open file: %s", file_path_.c_str());
      throw std::runtime_error("cannot open file");
    }

    // Subscribe to joint states (to track gripper joint)
    joint_state_sub_ = create_subscription<sensor_msgs::msg::JointState>(
      "/joint_states", 50,
      [this](const sensor_msgs::msg::JointState::SharedPtr msg)
      {
        std::lock_guard<std::mutex> lk(mutex_);
        for (size_t i = 0; i < msg->name.size(); ++i) {
          // cache gripper joint position if present
          if (msg->name[i] == gripper_joint_name_ && i < msg->position.size()) {
            gripper_pos_ = msg->position[i];
            break;
          }
        }
      });

    // Defer MoveGroupInterface creation until node is fully owned by shared_ptr
    init_timer_ = this->create_wall_timer(
      std::chrono::milliseconds(150),
      std::bind(&EefPoseAndGripperLogger::deferred_init, this));
  }

private:
  void deferred_init()
  {
    init_timer_->cancel();

    // Now safe to use shared_from_this()
    try {
      mgi_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
        this->shared_from_this(), group_);
    } catch (const std::exception& e) {
      RCLCPP_FATAL(get_logger(), "Failed to construct MoveGroupInterface: %s", e.what());
      throw;
    }

    eef_link_ = mgi_->getEndEffectorLink();
    if (eef_link_.empty()) {
      RCLCPP_WARN(get_logger(),
        "End-effector link is empty. MoveIt may not be fully configured for group '%s'. "
        "I will still attempt to log using getCurrentPose(group's EEF).", group_.c_str());
    }

    RCLCPP_INFO(get_logger(),
      "Logging EEF pose + gripper joint '%s' to %s at %.2f Hz (EEF link: %s, planning frame: %s)",
      gripper_joint_name_.c_str(), file_path_.c_str(), rate_hz_,
      eef_link_.empty() ? "<empty>" : eef_link_.c_str(),
      mgi_->getPlanningFrame().c_str());

    // Start periodic logging
    log_timer_ = this->create_wall_timer(period_, std::bind(&EefPoseAndGripperLogger::log_once, this));
  }

  void log_once()
  {
    // Get current EEF pose (if eef_link_ is empty, MoveIt still uses the group's EEF)
    geometry_msgs::msg::PoseStamped ps = mgi_->getCurrentPose(eef_link_);
    const auto& p = ps.pose.position;
    const auto& q = ps.pose.orientation;

    // Timestamp: prefer message stamp; fallback to node clock
    int32_t  sec  = ps.header.stamp.sec;
    uint32_t nsec = ps.header.stamp.nanosec;
    if (sec == 0 && nsec == 0) {
      const auto now = get_clock()->now();
      sec  = static_cast<int32_t>(now.seconds());
      nsec = static_cast<uint32_t>(now.nanoseconds() % 1000000000ULL);
    }

    double grip_val;
    {
      std::lock_guard<std::mutex> lk(mutex_);
      grip_val = gripper_pos_;
    }

    // Write one JSON object per line
    std::ostringstream js;
    js << std::fixed << std::setprecision(9);
    js << "{";
    js << "\"stamp\":{\"sec\":" << sec << ",\"nanosec\":" << nsec << "},";
    js << "\"frame_id\":\"" << ps.header.frame_id << "\",";
    js << "\"planning_frame\":\"" << mgi_->getPlanningFrame() << "\",";
    js << "\"eef_link\":\"" << (eef_link_.empty() ? "" : eef_link_) << "\",";
    js << "\"position\":{\"x\":" << p.x << ",\"y\":" << p.y << ",\"z\":" << p.z << "},";
    js << "\"orientation\":{\"x\":" << q.x << ",\"y\":" << q.y << ",\"z\":" << q.z << ",\"w\":" << q.w << "},";
    js << "\"gripper_joint\":{\"name\":\"" << gripper_joint_name_ << "\",\"position\":" << grip_val << "}";
    js << "}\n";

    ofs_ << js.str();
    ofs_.flush();
  }

  // Params
  std::string group_;
  std::string file_path_;
  std::string gripper_joint_name_;
  double rate_hz_{5.0};
  std::chrono::milliseconds period_{200};

  // State
  std::string eef_link_;
  double gripper_pos_{0.0};
  std::mutex mutex_;

  // ROS interfaces
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> mgi_;
  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_state_sub_;
  rclcpp::TimerBase::SharedPtr init_timer_;
  rclcpp::TimerBase::SharedPtr log_timer_;
  std::ofstream ofs_;
};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<EefPoseAndGripperLogger>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
