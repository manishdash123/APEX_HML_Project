#!/bin/bash


# Define the build directory
build_dir="build"

# Check if the build directory does not exist
if [ ! -d "$build_dir" ]; then
    # Make the build directory
    mkdir "$build_dir"
fi

# Go into the build directory
cd "$build_dir"

# Run CMake to configure the project
cmake ..

# Run CMake to build the project using all available cores
cmake --build . -j$(nproc)

