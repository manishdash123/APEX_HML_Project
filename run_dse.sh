
#!/bin/zsh

# Get the Arguments:

SRC_TACOS=$1
DEST_DIR=$2
DIM=$3
LINK=$4
BW=$5
CHUNK=$6
CHUNK_PER_COLL=$7

# Go into DEST DIR
cd $DEST_DIR

# <---------------------------------------------------------- CALL 1: TACOS --------------------------------------------------------->
echo "<------------------------------------------------------Calling TACOS ---------------------------------------------------------->"

TACOS_FILENAME=$(basename "$SRC_TACOS")

cp "$SRC_TACOS" "./$TACOS_FILENAME"

# Set execute permission for the binary file
chmod +x "./$TACOS_FILENAME"

# Now run the binary with the arguments and redirect the output to output.txt
./"$TACOS_FILENAME" "$DIM" "$LINK" "$BW" "$CHUNK" "$CHUNK_PER_COLL" > output.txt


# <---------------------------------------------------------- CALL 2: XML ---------------------------------------------------------->

python3 ../../analyze_network.py --K $DIM --link_lat $LINK --bw $BW --chunk_size $CHUNK --chunk_per_collective $CHUNK_PER_COLL --debug False


# <---------------------------------------------------------- CALL 3: CHAKRA -------------------------------------------------------->

# # make a directory for chakra outputs
# mkdir chakra_et

# # python3 -m et_converter.et_converter --input_type msccl --input_filename XX --output_filename XX
# python3 /home/davendra/project/chakra/et_converter/et_converter.py --input_type msccl --input_filename XX --output_filename XX

# <---------------------------------------------------------- CALL 4: ASTRASIM ------------------------------------------------------>


# BINARY=/home/davendra/project/astra-sim/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware

# SCRIPT_DIR=./

# WORKLOAD="${SCRIPT_DIR:?}"/inputs/workload/set_1/set_1

# # WORKLOAD="${SCRIPT_DIR:?}"/inputs/workload/test/one_comm_coll_node_allgather
# SYSTEM="${SCRIPT_DIR:?}"/inputs/system/Ring.json
# NETWORK="${SCRIPT_DIR:?}"/inputs/network/Mesh2D.yml
# MEMORY="${SCRIPT_DIR:?}"/inputs/remote_memory/no_memory_expansion.json

# "${BINARY}" \
#   --workload-configuration="${WORKLOAD}" \
#   --system-configuration="${SYSTEM}" \
#   --network-configuration="${NETWORK}"\
#   --remote-memory-configuration="${MEMORY}" > astrasim.txt



