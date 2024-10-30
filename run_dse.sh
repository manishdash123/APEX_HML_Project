
#!/bin/bash
# Get the Arguments:

SRC_TACOS="/home/karthike4/Desktop/apex/APEX_HML_Project/build/bin/TACOS"
DEST_DIR="/home/karthike4/Desktop/apex/APEX_HML_Project"
DIM=3
LINK=500
BW=50
CHUNK=1024
CHUNK_PER_COLL=2
# YAML_FILE=$8

# Go into DEST DIR
# cd $DEST_DIR

# #path to chakra folder
# export PYTHONPATH="/home/karthike4/Desktop/apex/chakra:$PYTHONPATH"

# # <---------------------------------------------------------- CALL 1: TACOS --------------------------------------------------------->
# # echo "<------------------------------------------------------Calling TACOS ---------------------------------------------------------->"

TACOS_FILENAME=$(basename "$SRC_TACOS")

cp "$SRC_TACOS" "./$TACOS_FILENAME"

# Set execute permission for the binary file
chmod +x "./$TACOS_FILENAME"

# Now run the binary with the arguments and redirect the output to output.txt
./"$TACOS_FILENAME" "$DIM" "$LINK" "$BW" "$CHUNK" "$CHUNK_PER_COLL" > output.txt


# # <---------------------------------------------------------- CALL 2: XML ---------------------------------------------------------->

python3 analyze_network.py --K $DIM --link_lat $LINK --bw $BW --chunk_size $CHUNK --chunk_per_collective $CHUNK_PER_COLL --debug 0 #--topology_dimensions 3


# <---------------------------------------------------------- CALL 3: CHAKRA -------------------------------------------------------->

# Construct the input filename
# INPUT_XML_FILENAME="gpu_${DIM}_link_${LINK}_bw_${BW}_chunk_${CHUNK}_chunk_coll_${CHUNK_PER_COLL}.xml"
# OUTPUT_ET_FILENAME="gpu_${DIM}_link_${LINK}_bw_${BW}_chunk_${CHUNK}_chunk_coll_${CHUNK_PER_COLL}"

# # Call the et_converter.py with the dynamically constructed filenames
# python3 -m et_converter.et_converter --input_type msccl \
# --input_filename gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.xml \
# --output_filename gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2 --num_dims 2

# python -m et_visualizer.et_visualizer\
#     --input_filename  /home/karthike4/Desktop/apex/APEX_HML_Project/gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.1.et \
#     --output_filename gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.1.pdf