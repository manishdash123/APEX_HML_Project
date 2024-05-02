# ECE/CS 8803 : Automated Parser for EXpanded Networks

This project has been done as part of the course project for the ECE /CS 8803 Hardware Software Co-design for Machine Learning Systems offered at Georgia Institute of Technology during Spring 2024 semester.

## Team Members
* [Davendra Seunarine Maharaj](https://github.com/davendramaharaj1)
* [Gaurav Singh Chandrabhan](https://github.com/Gauravchandrabhan)
* [Karthikeya Sharma](https://github.com/KarthikeyaSharma16)
* [Manish Dash](https://github.com/manishdash123)
* [Mohammad Zain](https://github.com/MZain-electro)

## Abstract
Collective communication techniques have played a significant role in optimizing the performance and power of interconnection networks. In today’s world, where the needto support a large number of interconnected devices in a network arises, these techniques have been instrumental in enhancing network bandwidth, optimizing performance, andreducing power consumption. Research works such as ASTRASIM and TACOS, which simulate collective communication on large distributed networks, can provide valuable insights into the importance of collective communication techniques and facilitate the development of further optimizations. However, there exists a gap between TACOS and ASTRA-SIM, which could potentially hinder research on collective communications. Moreover, since TACOS can synthesize collectives for arbitrary network topologies, the engineering effort to characterize these topologies to the system layer of ASTRA-SIM is both cumbersome and error-prone. As such, the aim of this work is to bridge the gap between TACOS and ASTRA-SIM by automating the design and simulation of collectives for a 2D Mesh Topology. Moreover, this work seeks to characterize the logical topological structure through the use of Chakra ET’s to facilitate a more streamlined and error-free analysis. Utilizing the simulations from ASTRASIM, Design Space Exploration (DSE) has been performed to explore the possible configurations of collectives that optimize for network performance. Additionally, extensive statistical analysis of the DSE results has been presented, providing insights into the effect of parameters such as bandwidth, mesh size, chunks per collective and chunk size on network performance.


## **Guidelines to run the entire automation code and perform Design Space Exploration (DSE)**

1) Clone the code from `node_traffic` branch (as that has been updated most recently).
2) In `run_dse.sh`, update the path of the Chakra ET converter where "PYTHONPATH" is assigned in line number 11.
   
4) In `run_dse.sh`, update the path for "BINARY" (which would be the path for the binary for ASTRAsim's analytical build).

   `BINARY=/home/davendra/project/astra-sim/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware` -> update this line.
   
6) In `dse.py`, update TACOS_SRC path as the path for the the binary file for TACOS (refer the "Guidelines to generate binary file for TACOS" on steps to generate the file).

   `TACOS_SRC = '/home/davendra/project/APEX_HML_Project/build/bin/TACOS'` -> update this line.
   
8) Specify the configurations for the network in `dse.py`:
   * Dimension (`K` Please note, **K** is the number of GPUs in one side of a square 2D mesh, so the total number of GPUs in the network would be K<sup>2</sup>)
   * Link latency (`link_latency`) (in GB/s)
   * Chunk Size `Chunk_size` (in MB)
   * Number of chunks per collective (`chunks_per_collective`)
     
9) Run the following command in a terminal : `python3 dse.py`.
    
11) The results will get populated in separate folders (for each configuration) in `./apex_outputs` folder.

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
