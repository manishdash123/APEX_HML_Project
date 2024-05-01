# APEX_HML_Project 
This project has been done as part of the course project for the EC 8803/ CS 8803 Hardware Sofware Codesign for Machine Learning course offered at Georgia Tech in Spring 2024 semester.

Automate integration of the bridge between [TACOS](https://arxiv.org/abs/2304.05301) and [ASTRA-SIM](https://astra-sim.github.io/). Automation of the Design Space Exploration (DSE) has also been done as part of the project.

Team Members
[Davendra Seunarine Maharaj](https://github.com/davendramaharaj1)
[Gaurav Singh Chandrabhan](https://github.com/Gauravchandrabhan)
[Karthikeya Sharma](https://github.com/KarthikeyaSharma16)
[Manish Dash](https://github.com/manishdash123)
[Mohammad Zain](https://github.com/MZain-electro)

**Guidelines to run the entire automation code and perform Design Space Exploration (DSE):**

1) Clone the code from node_traffic branch (as that has been updated most recently).
2) In run_dse.sh, update the path of the Chakra ET converter where "PYTHONPATH" is assigned.  
3) In run_dse.sh, update the path for "BINARY" (which would be the path for the binary for ASTRAsim's analytical build).
4) In dse.py, update TACOS_SRC path as the path for the the binary file for TACOS (refer the "Guidelines to generate binary file for TACOS" on steps to generate the file).  
5) Specify the configurations for the network, dimension (K), link_latency (in GB/s), chunk_size (in MB) and the number of chunks per collective (chunks_per_collective) in dse.py. Please note, K is the number of GPUs in one side of a square 2D mesh, so the total number of GPUs in the network would be K<sup>2</sup>. 
6) Run python3 dse.py.
7) Results will get populated in separate folders (for each configuration) in ./apex_outputs folder


**Guidelines to generate binary file for TACOS**:

Attached is the TACOS project source code for your project. Prerequisite is CMake v3.22. 

Please run it by:
tar -xf tacos-project.tar.xz

cd tacos

mkdir build

cd build

cmake ..

cmake --build . -j$(nproc)

./bin/TACOS

There are two code sections you might take a look into (as I mentioned, you can disregard other parts for the sake of the project). Those blocks are clearly marked by `FIXME:` directives.



•	runner/main.cpp: here you can set up 2D Mesh (size, link latency/bandwidth) and collective (All-Gather size and #chunks/collective)

•	synthesizer/TacosGreedy.cpp: here I'm printing the "[time] (chunk) src -> dest" information. I envision you may fix this, to dump data into files (e.g., yaml/json/txt/csv) then start parsing them to create the xml file.


Output run.sh to TACOS_output.txt from cmd terminal
