cmake_minimum_required(VERSION 3.8)
project(robotic_actions)


set(RMW_IMPLEMENTATION rmw_cyclonedds_cpp)


set(THIS_PACKAGE_INCLUDE_DEPENDS
  ament_cmake
  Boost
  control_msgs
  Eigen3
  interactive_markers
  moveit_core
  moveit_msgs
  moveit_ros_planning
  moveit_ros_planning_interface
  moveit_servo
  moveit_task_constructor_core
  moveit_visual_tools
  pluginlib
  rclcpp
  rclcpp_action
  rviz_visual_tools
  tf2_geometry_msgs
  tf2_geometry_msgs
  tf2_ros
)

foreach(Dependency IN ITEMS ${THIS_PACKAGE_INCLUDE_DEPENDS})
  find_package(${Dependency} REQUIRED)
endforeach()

include_directories(${THIS_PACKAGE_INCLUDE_DIRS})

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()
find_package(moveit_common REQUIRED)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(robotic_msgs REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(pluginlib REQUIRED)



# Add taskserver as a shared library
add_library(taskserver SHARED src/taskserver_joint_ankle_to_xyzrpy.cpp)
target_include_directories(taskserver PRIVATE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_definitions(taskserver PRIVATE TASKSERVER_CPP_BUILDING_DLL)

# Add pickandplace as a shared library
add_executable(robot_model_and_robot_state src/robot_model_and_robot_state.cpp)
ament_target_dependencies(robot_model_and_robot_state rclcpp moveit_ros_planning_interface tf2_geometry_msgs)


add_executable(add_object src/add_object.cpp)
ament_target_dependencies(add_object  rclcpp moveit_visual_tools moveit_ros_planning_interface  tf2_geometry_msgs  moveit_task_constructor_core)



# Define the executable
add_executable(demo_voice_command src/demo_voice_commands.cpp)
ament_target_dependencies(
  demo_voice_command  
  rclcpp moveit_visual_tools 
  moveit_ros_planning_interface  
  tf2_geometry_msgs  
  moveit_task_constructor_core 
  robotic_msgs)

# Define the executable for XYZRPY to XYZRPY
add_executable(task_server_xyzrpy_node src/taskserver_xyzrpy_to_xyzrpy.cpp)
ament_target_dependencies(
  task_server_xyzrpy_node  
  rclcpp moveit_visual_tools 
  moveit_ros_planning_interface  
  tf2_geometry_msgs  
  moveit_task_constructor_core 
  robotic_msgs)

install(TARGETS
task_server_xyzrpy_node
  DESTINATION lib/${PROJECT_NAME}
)
install(TARGETS
add_object
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS
demo_voice_command
  DESTINATION lib/${PROJECT_NAME}
)


# Install targets

install(TARGETS
robot_model_and_robot_state
  DESTINATION lib/${PROJECT_NAME})

ament_export_dependencies(
    ${THIS_PACKAGE_INCLUDE_DEPENDS}
  )
# Link libraries with dependencies
ament_target_dependencies(taskserver
  "rclcpp"
  "rclcpp_action"
  "robotic_msgs"
  "rclcpp_components"
  "geometry_msgs"
  "moveit_ros_planning_interface")

# Register taskserver as a component
rclcpp_components_register_node(taskserver
  PLUGIN "RoboticTasks::RoboticTaskServer"
  EXECUTABLE task_server_joint_ankle_to_xyzrpy_node)

# Install targets
install(TARGETS
  taskserver 
  robot_model_and_robot_state  
  add_object
  demo_voice_command
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)


# Uncomment the following if you want to install the additional scripts/files
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
install(
  PROGRAMS
  robotic_actions/alexa_interface.py
  DESTINATION lib/${PROJECT_NAME}/robotic_actions
)
# install(
#   PROGRAMS
#   robotic_actions/robotic_transformer_pytorch/robotic_transformer_pytorch.py
#   DESTINATION lib/${PROJECT_NAME}/
# )
# install(
#   PROGRAMS
#   robotic_actions/robotic_transformer_pytorch/pytorch_launch.py
#   DESTINATION lib/${PROJECT_NAME}/robotic_actions/robotic_transformer_pytorch/
# )
# install(
#   PROGRAMS
#   robotic_actions/robotic_transformer_pytorch/rt1_v1.pt
#   DESTINATION lib/${PROJECT_NAME}/robotic_actions/robotic_transformer_pytorch/
# )

# Testing and linting
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()
ament_export_include_directories(include)
ament_package()
