# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

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
CMAKE_COMMAND = /opt/homebrew/Cellar/cmake/3.28.3/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/Cellar/cmake/3.28.3/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/davendra/Downloads/tacos

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/davendra/Downloads/tacos/build

# Include any dependencies generated for this target.
include CMakeFiles/TACOS.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/TACOS.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/TACOS.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/TACOS.dir/flags.make

CMakeFiles/TACOS.dir/collective/AllGather.cpp.o: CMakeFiles/TACOS.dir/flags.make
CMakeFiles/TACOS.dir/collective/AllGather.cpp.o: /Users/davendra/Downloads/tacos/collective/AllGather.cpp
CMakeFiles/TACOS.dir/collective/AllGather.cpp.o: CMakeFiles/TACOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/TACOS.dir/collective/AllGather.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/TACOS.dir/collective/AllGather.cpp.o -MF CMakeFiles/TACOS.dir/collective/AllGather.cpp.o.d -o CMakeFiles/TACOS.dir/collective/AllGather.cpp.o -c /Users/davendra/Downloads/tacos/collective/AllGather.cpp

CMakeFiles/TACOS.dir/collective/AllGather.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/TACOS.dir/collective/AllGather.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/davendra/Downloads/tacos/collective/AllGather.cpp > CMakeFiles/TACOS.dir/collective/AllGather.cpp.i

CMakeFiles/TACOS.dir/collective/AllGather.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/TACOS.dir/collective/AllGather.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/davendra/Downloads/tacos/collective/AllGather.cpp -o CMakeFiles/TACOS.dir/collective/AllGather.cpp.s

CMakeFiles/TACOS.dir/collective/Collective.cpp.o: CMakeFiles/TACOS.dir/flags.make
CMakeFiles/TACOS.dir/collective/Collective.cpp.o: /Users/davendra/Downloads/tacos/collective/Collective.cpp
CMakeFiles/TACOS.dir/collective/Collective.cpp.o: CMakeFiles/TACOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/TACOS.dir/collective/Collective.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/TACOS.dir/collective/Collective.cpp.o -MF CMakeFiles/TACOS.dir/collective/Collective.cpp.o.d -o CMakeFiles/TACOS.dir/collective/Collective.cpp.o -c /Users/davendra/Downloads/tacos/collective/Collective.cpp

CMakeFiles/TACOS.dir/collective/Collective.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/TACOS.dir/collective/Collective.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/davendra/Downloads/tacos/collective/Collective.cpp > CMakeFiles/TACOS.dir/collective/Collective.cpp.i

CMakeFiles/TACOS.dir/collective/Collective.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/TACOS.dir/collective/Collective.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/davendra/Downloads/tacos/collective/Collective.cpp -o CMakeFiles/TACOS.dir/collective/Collective.cpp.s

CMakeFiles/TACOS.dir/helper/EventQueue.cpp.o: CMakeFiles/TACOS.dir/flags.make
CMakeFiles/TACOS.dir/helper/EventQueue.cpp.o: /Users/davendra/Downloads/tacos/helper/EventQueue.cpp
CMakeFiles/TACOS.dir/helper/EventQueue.cpp.o: CMakeFiles/TACOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/TACOS.dir/helper/EventQueue.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/TACOS.dir/helper/EventQueue.cpp.o -MF CMakeFiles/TACOS.dir/helper/EventQueue.cpp.o.d -o CMakeFiles/TACOS.dir/helper/EventQueue.cpp.o -c /Users/davendra/Downloads/tacos/helper/EventQueue.cpp

CMakeFiles/TACOS.dir/helper/EventQueue.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/TACOS.dir/helper/EventQueue.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/davendra/Downloads/tacos/helper/EventQueue.cpp > CMakeFiles/TACOS.dir/helper/EventQueue.cpp.i

CMakeFiles/TACOS.dir/helper/EventQueue.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/TACOS.dir/helper/EventQueue.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/davendra/Downloads/tacos/helper/EventQueue.cpp -o CMakeFiles/TACOS.dir/helper/EventQueue.cpp.s

CMakeFiles/TACOS.dir/helper/Timer.cpp.o: CMakeFiles/TACOS.dir/flags.make
CMakeFiles/TACOS.dir/helper/Timer.cpp.o: /Users/davendra/Downloads/tacos/helper/Timer.cpp
CMakeFiles/TACOS.dir/helper/Timer.cpp.o: CMakeFiles/TACOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/TACOS.dir/helper/Timer.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/TACOS.dir/helper/Timer.cpp.o -MF CMakeFiles/TACOS.dir/helper/Timer.cpp.o.d -o CMakeFiles/TACOS.dir/helper/Timer.cpp.o -c /Users/davendra/Downloads/tacos/helper/Timer.cpp

CMakeFiles/TACOS.dir/helper/Timer.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/TACOS.dir/helper/Timer.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/davendra/Downloads/tacos/helper/Timer.cpp > CMakeFiles/TACOS.dir/helper/Timer.cpp.i

CMakeFiles/TACOS.dir/helper/Timer.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/TACOS.dir/helper/Timer.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/davendra/Downloads/tacos/helper/Timer.cpp -o CMakeFiles/TACOS.dir/helper/Timer.cpp.s

CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.o: CMakeFiles/TACOS.dir/flags.make
CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.o: /Users/davendra/Downloads/tacos/synthesizer/TacosGreedy.cpp
CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.o: CMakeFiles/TACOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.o -MF CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.o.d -o CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.o -c /Users/davendra/Downloads/tacos/synthesizer/TacosGreedy.cpp

CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/davendra/Downloads/tacos/synthesizer/TacosGreedy.cpp > CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.i

CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/davendra/Downloads/tacos/synthesizer/TacosGreedy.cpp -o CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.s

CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.o: CMakeFiles/TACOS.dir/flags.make
CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.o: /Users/davendra/Downloads/tacos/synthesizer/TacosNetwork.cpp
CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.o: CMakeFiles/TACOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building CXX object CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.o -MF CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.o.d -o CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.o -c /Users/davendra/Downloads/tacos/synthesizer/TacosNetwork.cpp

CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/davendra/Downloads/tacos/synthesizer/TacosNetwork.cpp > CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.i

CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/davendra/Downloads/tacos/synthesizer/TacosNetwork.cpp -o CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.s

CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.o: CMakeFiles/TACOS.dir/flags.make
CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.o: /Users/davendra/Downloads/tacos/topology/Mesh2D.cpp
CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.o: CMakeFiles/TACOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building CXX object CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.o -MF CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.o.d -o CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.o -c /Users/davendra/Downloads/tacos/topology/Mesh2D.cpp

CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/davendra/Downloads/tacos/topology/Mesh2D.cpp > CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.i

CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/davendra/Downloads/tacos/topology/Mesh2D.cpp -o CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.s

CMakeFiles/TACOS.dir/topology/Topology.cpp.o: CMakeFiles/TACOS.dir/flags.make
CMakeFiles/TACOS.dir/topology/Topology.cpp.o: /Users/davendra/Downloads/tacos/topology/Topology.cpp
CMakeFiles/TACOS.dir/topology/Topology.cpp.o: CMakeFiles/TACOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building CXX object CMakeFiles/TACOS.dir/topology/Topology.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/TACOS.dir/topology/Topology.cpp.o -MF CMakeFiles/TACOS.dir/topology/Topology.cpp.o.d -o CMakeFiles/TACOS.dir/topology/Topology.cpp.o -c /Users/davendra/Downloads/tacos/topology/Topology.cpp

CMakeFiles/TACOS.dir/topology/Topology.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/TACOS.dir/topology/Topology.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/davendra/Downloads/tacos/topology/Topology.cpp > CMakeFiles/TACOS.dir/topology/Topology.cpp.i

CMakeFiles/TACOS.dir/topology/Topology.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/TACOS.dir/topology/Topology.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/davendra/Downloads/tacos/topology/Topology.cpp -o CMakeFiles/TACOS.dir/topology/Topology.cpp.s

CMakeFiles/TACOS.dir/runner/main.cpp.o: CMakeFiles/TACOS.dir/flags.make
CMakeFiles/TACOS.dir/runner/main.cpp.o: /Users/davendra/Downloads/tacos/runner/main.cpp
CMakeFiles/TACOS.dir/runner/main.cpp.o: CMakeFiles/TACOS.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Building CXX object CMakeFiles/TACOS.dir/runner/main.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/TACOS.dir/runner/main.cpp.o -MF CMakeFiles/TACOS.dir/runner/main.cpp.o.d -o CMakeFiles/TACOS.dir/runner/main.cpp.o -c /Users/davendra/Downloads/tacos/runner/main.cpp

CMakeFiles/TACOS.dir/runner/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/TACOS.dir/runner/main.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/davendra/Downloads/tacos/runner/main.cpp > CMakeFiles/TACOS.dir/runner/main.cpp.i

CMakeFiles/TACOS.dir/runner/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/TACOS.dir/runner/main.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/davendra/Downloads/tacos/runner/main.cpp -o CMakeFiles/TACOS.dir/runner/main.cpp.s

# Object files for target TACOS
TACOS_OBJECTS = \
"CMakeFiles/TACOS.dir/collective/AllGather.cpp.o" \
"CMakeFiles/TACOS.dir/collective/Collective.cpp.o" \
"CMakeFiles/TACOS.dir/helper/EventQueue.cpp.o" \
"CMakeFiles/TACOS.dir/helper/Timer.cpp.o" \
"CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.o" \
"CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.o" \
"CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.o" \
"CMakeFiles/TACOS.dir/topology/Topology.cpp.o" \
"CMakeFiles/TACOS.dir/runner/main.cpp.o"

# External object files for target TACOS
TACOS_EXTERNAL_OBJECTS =

bin/TACOS: CMakeFiles/TACOS.dir/collective/AllGather.cpp.o
bin/TACOS: CMakeFiles/TACOS.dir/collective/Collective.cpp.o
bin/TACOS: CMakeFiles/TACOS.dir/helper/EventQueue.cpp.o
bin/TACOS: CMakeFiles/TACOS.dir/helper/Timer.cpp.o
bin/TACOS: CMakeFiles/TACOS.dir/synthesizer/TacosGreedy.cpp.o
bin/TACOS: CMakeFiles/TACOS.dir/synthesizer/TacosNetwork.cpp.o
bin/TACOS: CMakeFiles/TACOS.dir/topology/Mesh2D.cpp.o
bin/TACOS: CMakeFiles/TACOS.dir/topology/Topology.cpp.o
bin/TACOS: CMakeFiles/TACOS.dir/runner/main.cpp.o
bin/TACOS: CMakeFiles/TACOS.dir/build.make
bin/TACOS: CMakeFiles/TACOS.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/Users/davendra/Downloads/tacos/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_10) "Linking CXX executable bin/TACOS"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/TACOS.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/TACOS.dir/build: bin/TACOS
.PHONY : CMakeFiles/TACOS.dir/build

CMakeFiles/TACOS.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/TACOS.dir/cmake_clean.cmake
.PHONY : CMakeFiles/TACOS.dir/clean

CMakeFiles/TACOS.dir/depend:
	cd /Users/davendra/Downloads/tacos/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/davendra/Downloads/tacos /Users/davendra/Downloads/tacos /Users/davendra/Downloads/tacos/build /Users/davendra/Downloads/tacos/build /Users/davendra/Downloads/tacos/build/CMakeFiles/TACOS.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/TACOS.dir/depend
