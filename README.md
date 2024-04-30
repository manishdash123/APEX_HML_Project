# APEX_HML_Project
TACOS-ASTRASIM HML project

**Guidelines to run the code:**

1) Specify the configurations in dse.py.
2) Run python3 dse.py.
3) Results will get populated in separate folders (for each configuration) in ./apex_outputs folder


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
