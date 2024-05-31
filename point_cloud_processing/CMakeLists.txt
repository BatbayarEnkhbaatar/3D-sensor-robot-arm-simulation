cmake_minimum_required(VERSION 3.8)
project(point_cloud_processing)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(PCL REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINATIONS})

add_executable(circular_cloud src/circular_point.cpp)
target_link_libraries(circular_cloud ${PCL_LIBRARIES})

add_executable(filtering src/filtering_segmentation.cpp)
target_link_libraries(filtering ${PCL_LIBRARIES})

add_executable(correspondence_grouping src/correspondence_grouping.cpp)
target_link_libraries(correspondence_grouping ${PCL_LIBRARIES})


add_executable(pass_through src/pass_through.cpp)
target_link_libraries(pass_through ${PCL_LIBRARIES})

install(TARGETS 
circular_cloud filtering pass_through correspondence_grouping
DESTINATION lib/${PROJECT_NAME})
ament_package()
