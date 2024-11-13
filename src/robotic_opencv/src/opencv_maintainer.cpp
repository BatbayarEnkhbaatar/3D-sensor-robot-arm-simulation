#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <filesystem>
#include <vector>
#include <sys/stat.h>
#include <ctime>
#include "ament_index_cpp/get_package_share_directory.hpp"

namespace fs = std::filesystem;
using namespace std::chrono_literals;

class maintainerNode: public rclcpp::Node
{
  public:
    maintainerNode()
    : Node("maintainer_FileChecker"), count_(0)
    {
      publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
      timer_ = this->create_wall_timer(
      500ms, std::bind(&maintainerNode::timer_callback, this));
    }

  private:
    struct FileInfo {
        std::string path;
        std::time_t creation_time;
    };

    std::time_t getFileCreationTime(const std::string& file_name) {
        struct stat t_stat;
        if (stat(file_name.c_str(), &t_stat) != 0) {
            perror("stat");
            return 0;
        }
        return t_stat.st_ctime;
    }

    void maintain_directory(const std::string& path) {
        std::vector<FileInfo> files;

        for (const auto& entry : fs::directory_iterator(path)) {
            std::string fileName = entry.path().string();
            std::time_t creationTime = getFileCreationTime(fileName);
            if (creationTime != 0) {
                files.push_back({fileName, creationTime});
            }
        }

        std::sort(files.begin(), files.end(), [](const FileInfo& a, const FileInfo& b) {
            return a.creation_time < b.creation_time;
        });

        while (files.size() > 100) {
            fs::remove(files.front().path);
            files.erase(files.begin());
        }

        std::cout << "Remaining files:\n";
        for (const auto& file : files) {
            std::cout << file.path << " (created on " << std::ctime(&file.creation_time) << ")";
        }
    }

    void timer_callback()
    {
      auto message = std_msgs::msg::String();
      RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
      publisher_->publish(message);


      std::string package_path = ament_index_cpp::get_package_share_directory("robotic_actions");
      std::string directory_path = fs::path(package_path) / "output";  
      maintain_directory(directory_path);
      message.data = "Maintainer Node is cleaning unnecessary frames from ... " + directory_path ;
    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    size_t count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<maintainerNode>());
  rclcpp::shutdown();
  return 0;
}
