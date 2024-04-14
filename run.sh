#!/bin/bash

# Check if /build/bin exists
if [ ! -d "/build/bin" ]; then
    echo "build/bin does not exist!"
    echo "Building TACOS..."

    # Run build.sh to presumably build the project and create /build/bin
    ./build.sh

    echo "TACOS build complete."
fi

# Go into the build/bin directory
cd /build/bin

# Run the TACOS executable
./TACOS

