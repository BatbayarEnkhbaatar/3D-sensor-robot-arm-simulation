cmake_minimum_required(VERSION 3.8)
project(robotic_action)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
# Uncomment the following section in order to fill in further dependencies manually.
# find_package(<dependency> REQUIRED)

find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(robotic_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclpy REQUIRED)

# PyTorch implementation
find_package(Torch REQUIRED)
include_directories(${TORCH_INCLUDE_DIRS})

add_library(task_server SHARED src/task_server.cpp)

target_include_directories(task_server PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
target_compile_definitions(task_server
  PRIVATE "TASK_SERVER_CPP_BUILDING_DLL"
)
target_link_libraries(task_server "${TORCH_LIBRARIES}")

ament_target_dependencies(task_server
  "robotic_msgs"
  "rclcpp"
  "rclcpp_action"
  "rclcpp_components"
  "moveit_ros_planning_interface"
)

rclcpp_components_register_node(task_server
  PLUGIN "RoboticActions::TaskServerNode"
  EXECUTABLE task_server_node
)

ament_python_install_package(${PROJECT_NAME})

install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
install(
  PROGRAMS
  robotic_action/rest_api.py
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS
  task_server
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
