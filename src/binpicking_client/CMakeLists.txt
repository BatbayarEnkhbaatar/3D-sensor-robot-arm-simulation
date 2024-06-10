cmake_minimum_required(VERSION 3.8)
project(binpicking_client)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)

add_executable(binpicking_client_node src/binpicking_client_node.cpp)

ament_target_dependencies(binpicking_client_node rclcpp spdlog)

target_link_libraries(binpicking_client_node fmt::fmt spdlog::spdlog)

install(TARGETS
  binpicking_client_node
  DESTINATION lib/${PROJECT_NAME})

ament_package()