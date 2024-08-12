#!/bin/bash
set -e

SCRIPT_DIR=$(dirname "$(realpath $0)")
BINARY="${SCRIPT_DIR:?}"/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware
WORKLOAD="${SCRIPT_DIR:?}"/inputs/workload/set_1
# WORKLOAD="${SCRIPT_DIR:?}"/inputs/workload/test/one_comm_coll_node_allgather
SYSTEM="${SCRIPT_DIR:?}"/inputs/system/Ring.json
NETWORK="${SCRIPT_DIR:?}"/inputs/network/Mesh2D.yml
MEMORY="${SCRIPT_DIR:?}"/inputs/remote_memory/no_memory_expansion.json

"${BINARY}" \
  --workload-configuration="${WORKLOAD}" \
  --system-configuration="${SYSTEM}" \
  --network-configuration="${NETWORK}"\
  --remote-memory-configuration="${MEMORY}"
