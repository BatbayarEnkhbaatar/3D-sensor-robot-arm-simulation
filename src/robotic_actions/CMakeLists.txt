cmake_minimum_required(VERSION 3.8)
project(robotic_actions)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
###customer packages are here
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(robotic_msgs REQUIRED)
find_package(rclcpp_components REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# add_executable(taskserver src/taskserver.cpp)
add_library(taskserver SHARED src/taskserver.cpp)
target_include_directories(taskserver PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
  target_compile_definitions(taskserver PRIVATE TASKSERVER_CPP_BUILDING_DLL)  # Require C99 and C++17


#Customer Declaration

ament_target_dependencies(taskserver
  "rclcpp"
  "rclcpp_action"
  "robotic_msgs"
  "rclcpp_components")
  rclcpp_components_register_node(taskserver
  PLUGIN "RoboticTasks::TaskServer"
  EXECUTABLE taskservernode)

install(TARGETS
  taskserver
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

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
