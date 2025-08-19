cmake_minimum_required(VERSION 3.8)
project(yaskawa_pick_place_demo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(trajectory_msgs REQUIRED)
find_package(linkattacher_msgs REQUIRED)
find_package(robotic_msgs REQUIRED)
add_executable(yaskawa_pick_place_demo src/yaskawa_pick_place_demo.cpp)


find_package(trajectory_msgs REQUIRED)



target_include_directories(yaskawa_pick_place_demo PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(yaskawa_pick_place_demo PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  yaskawa_pick_place_demo
  "rclcpp"
  "moveit_ros_planning_interface"
  "trajectory_msgs"
  "linkattacher_msgs"
  "robotic_msgs"
)


add_executable(gripper_test_node src/gripper_control.cpp)
ament_target_dependencies(gripper_test_node rclcpp trajectory_msgs)

install(TARGETS
  gripper_test_node
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS yaskawa_pick_place_demo
  DESTINATION lib/${PROJECT_NAME})


  # Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
