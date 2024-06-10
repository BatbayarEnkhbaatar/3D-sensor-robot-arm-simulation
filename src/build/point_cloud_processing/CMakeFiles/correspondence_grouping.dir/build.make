# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ubuntu/robot-simulation/src/point_cloud_processing

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ubuntu/robot-simulation/src/build/point_cloud_processing

# Include any dependencies generated for this target.
include CMakeFiles/correspondence_grouping.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/correspondence_grouping.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/correspondence_grouping.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/correspondence_grouping.dir/flags.make

CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.o: CMakeFiles/correspondence_grouping.dir/flags.make
CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.o: /home/ubuntu/robot-simulation/src/point_cloud_processing/src/correspondence_grouping.cpp
CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.o: CMakeFiles/correspondence_grouping.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ubuntu/robot-simulation/src/build/point_cloud_processing/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.o -MF CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.o.d -o CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.o -c /home/ubuntu/robot-simulation/src/point_cloud_processing/src/correspondence_grouping.cpp

CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ubuntu/robot-simulation/src/point_cloud_processing/src/correspondence_grouping.cpp > CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.i

CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ubuntu/robot-simulation/src/point_cloud_processing/src/correspondence_grouping.cpp -o CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.s

# Object files for target correspondence_grouping
correspondence_grouping_OBJECTS = \
"CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.o"

# External object files for target correspondence_grouping
correspondence_grouping_EXTERNAL_OBJECTS =

correspondence_grouping: CMakeFiles/correspondence_grouping.dir/src/correspondence_grouping.cpp.o
correspondence_grouping: CMakeFiles/correspondence_grouping.dir/build.make
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_apps.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_outofcore.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_people.so
correspondence_grouping: /usr/lib/libOpenNI.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libusb-1.0.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libOpenNI2.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libusb-1.0.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libflann_cpp.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_surface.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_keypoints.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_tracking.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_recognition.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_registration.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_stereo.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_segmentation.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_features.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_filters.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_sample_consensus.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_ml.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_visualization.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_search.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_kdtree.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_io.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_octree.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpng.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libz.so
correspondence_grouping: /usr/lib/libOpenNI.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libusb-1.0.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libOpenNI2.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkChartsCore-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkInteractionImage-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkIOGeometry-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libjsoncpp.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkIOPLY-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkRenderingLOD-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkViewsContext2D-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkViewsCore-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkGUISupportQt-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkInteractionWidgets-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkFiltersModeling-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkInteractionStyle-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkFiltersExtraction-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkIOLegacy-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkIOCore-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkRenderingAnnotation-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkRenderingContext2D-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkRenderingFreeType-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libfreetype.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkImagingSources-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkIOImage-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkImagingCore-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkRenderingOpenGL2-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkRenderingUI-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkRenderingCore-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkCommonColor-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkFiltersGeometry-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkFiltersSources-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkFiltersGeneral-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkCommonComputationalGeometry-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkFiltersCore-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkCommonExecutionModel-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkCommonDataModel-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkCommonMisc-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkCommonTransforms-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkCommonMath-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkkissfft-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libGLEW.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libX11.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libQt5OpenGL.so.5.15.3
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libQt5Widgets.so.5.15.3
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libQt5Gui.so.5.15.3
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libQt5Core.so.5.15.3
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtkCommonCore-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libtbb.so.12.5
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libvtksys-9.1.so.9.1.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libpcl_common.so
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libboost_system.so.1.74.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.74.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libboost_date_time.so.1.74.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libboost_iostreams.so.1.74.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libboost_serialization.so.1.74.0
correspondence_grouping: /usr/lib/x86_64-linux-gnu/libqhull_r.so.8.0.2
correspondence_grouping: CMakeFiles/correspondence_grouping.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ubuntu/robot-simulation/src/build/point_cloud_processing/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable correspondence_grouping"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/correspondence_grouping.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/correspondence_grouping.dir/build: correspondence_grouping
.PHONY : CMakeFiles/correspondence_grouping.dir/build

CMakeFiles/correspondence_grouping.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/correspondence_grouping.dir/cmake_clean.cmake
.PHONY : CMakeFiles/correspondence_grouping.dir/clean

CMakeFiles/correspondence_grouping.dir/depend:
	cd /home/ubuntu/robot-simulation/src/build/point_cloud_processing && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ubuntu/robot-simulation/src/point_cloud_processing /home/ubuntu/robot-simulation/src/point_cloud_processing /home/ubuntu/robot-simulation/src/build/point_cloud_processing /home/ubuntu/robot-simulation/src/build/point_cloud_processing /home/ubuntu/robot-simulation/src/build/point_cloud_processing/CMakeFiles/correspondence_grouping.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/correspondence_grouping.dir/depend

