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

# <---------------------------------------------------------- CALL 3: CHAKRA -------------------------------------------------------->
# Construct the input filename
INPUT_XML_FILENAME="gpu_${DIM}_link_${LINK}_bw_${BW}_chunk_${CHUNK}_chunk_coll_${CHUNK_PER_COLL}_dimensions_${DIMENSIONS}.xml"
OUTPUT_ET_FILENAME="gpu_${DIM}_link_${LINK}_bw_${BW}_chunk_${CHUNK}_chunk_coll_${CHUNK_PER_COLL}_dimensions_${DIMENSIONS}"

# # Call the et_converter.py with the dynamically constructed filenames
python3 -m chakra.et_converter.et_converter --input_type msccl \
--input_filename "$INPUT_XML_FILENAME" \
--output_filename "$OUTPUT_ET_FILENAME" --num_dims 3

# python -m et_visualizer.et_visualizer\
#     --input_filename  /home/karthike4/Desktop/apex/APEX_HML_Project/gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.1.et \
#     --output_filename gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.1.pdf