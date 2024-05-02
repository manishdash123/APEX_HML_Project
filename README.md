# ECE/CS 8803 : Automated Parser for EXpanded Networks

This project has been done as part of the course project for the ECE /CS 8803 Hardware Software Co-design for Machine Learning Systems offered at Georgia Institute of Technology during Spring 2024 semester.

## Team Members
* [Davendra Seunarine Maharaj](https://github.com/davendramaharaj1)
* [Gaurav Singh Chandrabhan](https://github.com/Gauravchandrabhan)
* [Karthikeya Sharma](https://github.com/KarthikeyaSharma16)
* [Manish Dash](https://github.com/manishdash123)
* [Mohammad Zain](https://github.com/MZain-electro)

## Abstract
Collective communication techniques have played a significant role in optimizing the performance and power of interconnection networks. In today’s world, where the need to support a large number of interconnected devices in a network arises, these techniques have been instrumental in enhancing network bandwidth, optimizing performance, and reducing power consumption. Research works such as ASTRASIM and TACOS, which simulate collective communication on large distributed networks, can provide valuable insights into the importance of collective communication techniques and facilitate the development of further optimizations. However, there exists a gap between TACOS and ASTRA-SIM, which could potentially hinder research on collective communications. Moreover, since TACOS can synthesize collectives for arbitrary network topologies, the engineering effort to characterize these topologies to the system layer of ASTRA-SIM is both cumbersome and error-prone. As such, the aim of this work is to bridge the gap between TACOS and ASTRA-SIM by automating the design and simulation of collectives for a 2D Mesh Topology. Moreover, this work seeks to characterize the logical topological structure through the use of Chakra ET’s to facilitate a more streamlined and error-free analysis. Utilizing the simulations from ASTRASIM, Design Space Exploration (DSE) has been performed to explore the possible configurations of collectives that optimize for network performance. Additionally, extensive statistical analysis of the DSE results has been presented, providing insights into the effect of parameters such as bandwidth, mesh size, chunks per collective and chunk size on network performance.

## **Motivation**
* Gap between TACOS and ASTRA-SIM hinders the ability to quickly develop and simulate the performance of different collectives on network topologies
* Difficult and cumbersome to describe the characteristics of the desired system layer of Astra-Sim for arbitrary topologies
* Lack of exploration to determine optimal configurations of collectives for arbitrary network topologie

## **Goals**
* Develop a workaround to bypass the system layer for smooth and efficient integration of TACOS with ASTRA-SIM with the help of CHAKRA Execution Traces (ETs)
* Explore the design space of a NPU-based network executing an All Gather collective communication algorithms within a 2D mesh topology

## **Contributions**
* Created an automated toolchain to bridge the gap between synthesis of collective communication algorithms for arbitrary topologies by bypassing the system layer of Astra-Sim. This projeAt is mainly focused on all gather collectives.
* Conducted DSE over different collective configurations to explore the space for finding configurations in understanding performance impact on a given topology

## **Directory Structure**
```.
├── TACOS_output.txt
├── analyze_network.py
├── build
│   ├── Makefile
│   ├── bin
│   │   ├── TACOS
│   │   └── output.csv
│   └── cmake_install.cmake
├── build_bash.sh
├── dse.py
├── inputs
│   ├── network
│   │   └── Mesh2D.yml
│   ├── remote_memory
│   │   └── no_memory_expansion.json
│   └── system
│       └── Ring.json
├── network_analysis.ipynb
├── network_flow_pretty_base.xml
├── network_model.ipynb
├── preprocessed_output.csv
├── results.ipynb
├── run.sh
├── run_dse.sh
├── runner
│   └── main.cpp
├── runtime_analysis.csv
├── synthesizer
│   ├── TacosGreedy.cpp
│   └── TacosNetwork.cpp
└── topology
    ├── Mesh2D.cpp
    └── Topology.cpp
```
    
1) The Automation scripts for this project are:
   - dse.py
   - run_dse.sh (Ensure to change ```#!/bin/zsh``` to ```#!/bin/bash``` if you are using bash)
2) For some combination of parameters when running DSE:
   - an output directory called './apex_outputs' is created in the root directory
   - Within ```./apex_outputs```, a sub directory for the configuration is created with the following the naming conventions: 
      - ``` gpu_{K}_link_{link_lat}_bw_{bw}_chunk_{chunk_size}_chunk_coll_{chunk_per_collective} ```
3) When running dse.py, the inputs to Astra-Sim (for system layer and remote memory layer) are assumed to be in the root directory of thi repository in a folder called ```inputs```
4) Depending on the choice of mesh size, bandwidth and latency, a yaml file for the network backend is generated in the configuration sub-directory of ```./apex_outputs```
5) The TACOS binary is built in the directory ``` ./build/bin```
   - For each DSE run, the ``` ./build/bin/TACOS``` binary is copied into the configuration output folder. The following 2 files are produced to parse collective information:
      - output.txt : Summary of TACOS output
      - output.csv : TENs representation of network flow in csv format
6) After a DSE run, the Astra-Sim output text file for a particular configuration is produced in the configuration output folder with the same naming convention as it's parent directory:
   -  ``` gpu_{K}_link_{link_lat}_bw_{bw}_chunk_{chunk_size}_chunk_coll_{chunk_per_collective}_astrasim.txt ```

## **Prerequisites**
1) Clone the ASTRASIM `main` branch from https://github.com/astra-sim/astra-sim .
2) Setup ASTRASIM based on the guidelines at https://astra-sim.github.io/astra-sim-docs/getting-started/setup.html .
3) Make changes in the ASTRASIM folder as per the instructions given in the UPDATE_astrasim.md file in update_ASTRAsim.zip.
4) Clone the CHAKRA `mscclang_converter` branch from https://github.com/jinsun-yoo/chakra/tree/mscclang_converter .

   Note: Do a `git checkout mscclang_converter` to switch the branch from main to mscclang_converter branch.
5) Setup CHAKRA based on the guidelines at https://github.com/jinsun-yoo/chakra/blob/mscclang_converter/INSTALL.md .


## **Guidelines to run the entire automation code and perform Design Space Exploration (DSE)**

1) Clone the code from `node_traffic` branch.

2) In `run_dse.sh`, update Line 11 where the path of the Chakra ET converter "PYTHONPATH" is assigned.
   
3) In `run_dse.sh`, update the path at Line 59 for "BINARY" (which would be the path for the binary for ASTRAsim's analytical build).
   
4) In `dse.py`, update the path at Line 25 for "TACOS_SRC" as the path for the the binary file for TACOS (refer the "Guidelines to generate binary file for TACOS" on steps to generate the file).
   
   Hint: Use `pwd` command for finding the paths of Chakra ET, ASTRAsim's analytical build and TACOS_SRC.
   
5) Specify the configurations for the network in `dse.py`:
   * Dimension (`K`) (Please note, **K** is the number of GPUs in one side of a square 2D mesh, so the total number of GPUs in the network would be K<sup>2</sup>)
   * Link latency (`link_latency`) (in GB/s)
   * Chunk Size (`chunk_size`) (in MB)
   * Number of chunks per collective (`chunks_per_collective`)
     
6) Run the following command in a terminal : `python3 dse.py`.
    
7) The results will get populated in separate folders (for each configuration) in `./apex_outputs` folder.

## **Guidelines to generate binary file for TACOS**
Attached is the TACOS project source code for your project. Prerequisite is CMake v3.22. 

#### Set of commands to run TACOS is given below:
* `tar -xf tacos-project.tar.xz`
* `cd tacos`
* `mkdir build`
* `cd build`
* `cmake ..`
* `cmake --build . -j$(nproc)`
* `./bin/TACOS`

**However, the above set of commands has been automated by writing a separate bash script `run.sh`, and stores the binary in `/build/bin/TACOS`**

## References
* [TACOS](https://arxiv.org/abs/2304.05301)
* [ASTRA-SIM](https://astra-sim.github.io/)
* [Chakra](https://github.com/mlcommons/chakra)
* [MSCClang Converter](https://github.com/jinsun-yoo/chakra/tree/mscclang_converter)
