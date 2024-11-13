#include <cstdio>
#include <filesystem>
#include <rclcpp/rclcpp.hpp>
#include "sensor_msgs/msg/image.hpp"
#include "cv_bridge/cv_bridge.h"
#include "opencv2/opencv.hpp"
#include "ament_index_cpp/get_package_share_directory.hpp"
#include <chrono>
#include <iomanip>
#include <ctime>
#include <sstream> // Needed for std::ostringstream

namespace fs = std::filesystem;

class OpenCVNode : public rclcpp::Node 
{
public:
  OpenCVNode() : Node("opencv_node"), image_counter_(0)
  {
    // Get the current working directory and append the "output" directory
    std::string package_path = ament_index_cpp::get_package_share_directory("robotic_actions");
    save_directory_ = fs::path(package_path) / "output";

    // Create the save directory if it doesn't exist
    if (!fs::exists(save_directory_)) {
      fs::create_directory(save_directory_);
    }

    subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
      "/TesseraVue/image_raw", 10, std::bind(&OpenCVNode::image_callback, this, std::placeholders::_1)
    );
  }

private:
  std::string getCurrentTimeStamp() const
  {
    // Get current time
    auto now = std::chrono::system_clock::now();
    
    // Convert to time_t to get the time in seconds since the epoch
    std::time_t currentTime = std::chrono::system_clock::to_time_t(now);
    
    // Convert to tm structure for local time
    std::tm* localTime = std::localtime(&currentTime);
    
    // Create a string stream to format the time
    std::ostringstream oss;
    oss << std::put_time(localTime, "%Y%m%d%H%M%S");
    
    // Return the formatted string
    return oss.str();
  }

  void image_callback(const sensor_msgs::msg::Image::SharedPtr msg) const
  {
    try 
    {
      cv::Mat frame = cv_bridge::toCvShare(msg, "bgr8")->image;
      // cv::imshow("Camera", frame);
      cv::waitKey(200);
      std::string timestampsName = getCurrentTimeStamp(); // Add missing semicolon
      // Save the image to a file in the output directory
      std::string filename = (save_directory_ / ("frame_" + timestampsName + ".jpg")).string();
      cv::imwrite(filename, frame);
      // RCLCPP_INFO(this->get_logger(), "Saved image: %s", filename.c_str());

      // Increment the image counter
      image_counter_++;
    }
    catch (cv_bridge::Exception& e)
    {
      RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
    }
  }

  mutable int image_counter_; // Counter to generate unique filenames
  fs::path save_directory_; // Path to the save directory
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscription_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<OpenCVNode>());
  rclcpp::shutdown();
  return 0;
}
