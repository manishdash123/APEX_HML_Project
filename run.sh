#!/bin/bash

# Check if /build/bin exists
if [ ! -d "/build/bin" ]; then
    echo "build/bin does not exist!"
    echo "Building TACOS..."

    # Run build.sh to presumably build the project and create /build/bin
    ./build_bash.sh

    echo "TACOS build complete."
fi

# Go into the build/bin directory
cd ./build/bin

# Run the TACOS executable
./TACOS 3 500 50 1024 2 > ./../../TACOS_output.txt

echo "TACOS saved to TACOS_output"
