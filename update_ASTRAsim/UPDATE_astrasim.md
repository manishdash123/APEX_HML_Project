### Environment Tested
- macOS 14.4.1 (if using Linux, please ping me back but I don't expect much changes)
- Python 3.7.16
- Protobuf 3.8.0
- With sudo access (to install Protobuf; you can instead just add to PATH/LD_LIBRARY_PATH)

### Prerequisite
1. Download and compile protobuf 3.8.0
- Hosted here: https://github.com/protocolbuffers/protobuf/releases/tag/v3.8.0
```sh
$ wget https://github.com/protocolbuffers/protobuf/releases/download/v3.8.0/protobuf-all-3.8.0.tar.gz
$ tar -xf protobuf-all-3.8.0.tar.gz
$ cd protobuf-3.8.0
$ ./configure
$ make -j$(nproc)
$ make check -j$(nproc)  # checking compilation finished successfully
$ sudo make install  # register protobuf to PATH
$ which protoc  # system should be able to locate protoc
```

2. Setup Python environment (I'm using miniconda3)
```sh
$ conda create -n astra-sim python=3.7
$ conda activate astra-sim
$ conda install protobuf=3.8.0 graphviz python-graphviz pydot networkx
$ protoc --version  # should show libprotoc 3.8.0
```

### ASTRA-sim Patch and Installation
1. Cloning and compiling ASTRA-sim (with congestion-aware analytical backend)
```sh
$ git clone --recurse-submodules git@github.com:astra-sim/astra-sim.git  # or use https protocol
$ cd astra-sim
```

2. (To be done for MAC OS, and to be skipped for Linux OS like Ubuntu)
For `et_feeder.h`, fix `std::binary_function<>` into `std::__binary_function<>` (tested on macOS, not sure about linux)
```sh
$ vim ./extern/graph_frontend/chakra/et_feeder/et_feeder.h
# change line 13 to:
# struct CompareNodes: public std::__binary_function<std::shared_ptr<ETFeederNode>, std::shared_ptr<ETFeederNode>, bool>
```

3. Disable `COMPILE_WARNING_AS_ERROR` flag in top level CMakeLists.txt
```sh
$ vim ./CMakeLists.txt
# Comment out or remove line 45
# # set_target_properties(AstraSim PROPERTIES COMPILE_WARNING_AS_ERROR ON)
```

4. Patch Mesh2D implementation
- Remove `./extern/network_backend/analytical` folder and paste the provided `analytical` codebase, which includes Mesh2D implementation.

5. Patch inputs and run scripts
- At the top directory replace the `inputs/` directory with the provided one. Also, put `run.sh` as well.


6. Paste and apply the patch, 0001-Release-constraint-for-COMM_RECV-nodes.patch in the root directoy of ASTRAsim.

7. Go to `astra-sim/extern/graph_frontend/chakra/et_feeder` and update line 11 to this->is_cpu_op_ = false;

8. Compile ASTRA-sim
```sh
$ ./build/astra_analytical/build.sh
```

### Running ASTRA-sim
1. Give `run.sh` the execute permission
```sh
$ chmod +x ./run.sh
```

2. Run compiled ASTRA-sim
```sh
$ ./run.sh
```

- To test other configurations:
    - Change `./inputs/network/Mesh2D.yml` to adjust the Mesh size (currently, only square Mesh like 9, 16, 25, ..., are supported), bandwidth and latency per each link.
    - Paste your generated `.et` files in `inputs/workload/` and change the filename in `./run.sh`. For your reference I've provided `/inputs/workload/test/one_comm_coll_node_allgather` workload.
