#!/bin/bash

# <------------------------------------------------ RUN APEX ---------------------------------------------------------------------->
SRC_TACOS="/home/karthike4/Desktop/apex/APEX_HML_Project/build/bin/TACOS"
DEST_DIR="/home/karthike4/Desktop/apex/APEX_HML_Project"
DIM=2
LINK=500
BW=50
CHUNK=1024
CHUNK_PER_COLL=2
DIMENSIONS=3

# Ensure the TACOS binary exists before trying to execute
if [ -f "$SRC_TACOS" ]; then
    "$SRC_TACOS" "$DIM" "$LINK" "$BW" "$CHUNK" "$CHUNK_PER_COLL" > "$DEST_DIR/output.txt"
else
    echo "Error: TACOS binary not found at $SRC_TACOS"
    exit 1
fi

# # <--------------------------------------------------------- RUN APEX ---------------------------------------------------------->

# Run analyze_network.py if it exists
if [ -f "analyze_network.py" ]; then
    python3 analyze_network.py --K "$DIM" --link_lat "$LINK" --bw "$BW" --chunk_size "$CHUNK" --chunk_per_collective "$CHUNK_PER_COLL" --debug 0 --topology_dimensions "$DIMENSIONS"
else
    echo "Error: analyze_network.py not found"
fi

# <--------------------------------------------------- RUN VISUALIZER ------------------------------------------------------------>

# Run main.py if it exists
if [ -f "main.py" ]; then
    python3 main.py
else
    echo "Error: main.py not found"
fi

# <------- REMOVE UNNECESSARY FILES ------> 
rm ./TACOS output.txt output.csv

# Open plot_viewer.html if it exists
if [ -f "plot_viewer.html" ]; then
    xdg-open plot_viewer.html
else
    echo "Error: plot_viewer.html not found"
fi

rm -rf Plots/