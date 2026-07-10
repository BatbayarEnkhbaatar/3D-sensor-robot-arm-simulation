cmake_minimum_required(VERSION 3.8)
project(yaskawa_mh5_task_node)

# Optional: pick a standard
# set(CMAKE_CXX_STANDARD 17)
# set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(yaskawa_msgs REQUIRED)
find_package(robotic_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)

# 1..===== Arm task server component =====
add_library(task_server_arm SHARED src/task_server_robot_arm_node.cpp)
target_include_directories(task_server_arm PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(task_server_arm
  rclcpp
  rclcpp_action
  rclcpp_components
  yaskawa_msgs
  robotic_msgs
  moveit_ros_planning_interface
)
# Adjust PLUGIN string to match the fully-qualified class name in your .cpp
rclcpp_components_register_node(task_server_arm
  PLUGIN "RoboticTasks::RoboticTaskServer"
  EXECUTABLE task_server_arm_node
)



#2.. ===== Gripper task server component =====
add_library(task_server_gripper SHARED src/task_server_gripper_node.cpp)
target_include_directories(task_server_gripper PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
ament_target_dependencies(task_server_gripper
  rclcpp
  rclcpp_action
  rclcpp_components
  yaskawa_msgs
  robotic_msgs
  moveit_ros_planning_interface
)

# 3.get eef pose 

add_executable(eef_pose_printer_node src/get_eef_pose.cpp)
ament_target_dependencies(eef_pose_printer_node
  rclcpp
  moveit_ros_planning_interface
)

install(TARGETS eef_pose_printer_node
  DESTINATION lib/${PROJECT_NAME}
)


# Adjust PLUGIN string to match the fully-qualified class name in your gripper .cpp
rclcpp_components_register_node(task_server_gripper
  PLUGIN "RoboticTasks::GripperTaskServer"
  EXECUTABLE task_server_gripper_node
)

# Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

# Install headers if you have any
install(DIRECTORY include/
  DESTINATION include
)

# Install package.xml so the package is discoverable at runtime
install(FILES package.xml
  DESTINATION share/${PROJECT_NAME}
)


# Install libraries and auto-generated executables
install(TARGETS
  task_server_arm
  task_server_gripper
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
