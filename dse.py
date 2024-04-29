import os
import shutil
import subprocess
import numpy as np
import concurrent.futures
from itertools import product


def clean_directory(directory):
    # This function removes all files and folders in the specified directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Define the function that will call in parallel
def run_analysis(K, link_lat, bw, chunk_size, chunk_per_collective):

    TACOS_SRC = os.path.join('/home/davendra/project/APEX_HML_Project/build/bin/TACOS')

    ROOT_DIR = os.path.join('./apex_outputs')
    OUTPUT_DIR = f'gpu_{K}_link_{link_lat}_bw_{bw}_chunk_{chunk_size}_chunk_coll_{chunk_per_collective}'

    OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_DIR)

    # Ensure the output directory is clean
    if os.path.exists(OUTPUT_PATH):
        print(f'Directory: {OUTPUT_PATH} alreadY exists!')
        print(f'Cleaning {OUTPUT_PATH}...\n')
        clean_directory(OUTPUT_PATH)
        print(f'Done cleaning {OUTPUT_PATH}\n')
    else:
        try: 
            os.makedirs(OUTPUT_PATH) 
        # print("Directory '%s' created successfully" % OUTPUT_PATH) 
        except OSError as error: 
            print("Directory '%s' can not be created" % OUTPUT_PATH)

    command = f"./run_dse.sh {TACOS_SRC} {OUTPUT_PATH} {K} {link_lat} {bw} {chunk_size} {chunk_per_collective}"

    # Run the command
    subprocess.run(command, shell=True)



run_analysis(3, 500, 50, 1024, 1)

    # 1. run tacos script ----> produce: output.csv & output.txt
    # 2. run analysis script ------> xml
    # 3. run the chakra conversion script -----> ET's
    # 4. run astra-sim -----> pipe to text OR use a python subprocess and make a csv
    # pass

    # Call TACOS to generate network flow -------> output.csv & output.txt
    # Call XML_Geneator to create XML format --------> input: output.csv, output.txt, intermediate: preprocess.csv, output: network.xml
    # Call Chakra to use XML and generate Traces -------> input: network.xml, output: *.et
    # Call Astrasim to use traces and give results as a txt file --------> input: *.et, output: astrasim.txt

# Create a list of all possible combinations of the variables
# gpu_mesh_sizes = [(i, i) for i in range(2, 101)]  # Creates tuples like (2, 2), (3, 3), etc.

# # NV: 
# link_latency = list(range(500, 10000, 500))  # 200, 300, ..., 1000
# bandwidths = list(range(50, 1000, 50))  # 10, 20, ..., 80
# chunk_size = list(range(0.001, 10000, 500))

# # Generate all combinations of parameters
# param_combinations = list(product(gpu_mesh_sizes, link_latency, bandwidths))

# # Function to unpack arguments
# def run_with_params(params):
#     return run_analysis(*params)

# # Run the tasks in parallel using ProcessPoolExecutor
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     # Map the run_with_params to the list of parameter combinations
#     results = list(executor.map(run_with_params, param_combinations))


# K = 16, 64, 144, 256, 400 <--------> Zain, Gaurav, Manish, Karthik, Davendra