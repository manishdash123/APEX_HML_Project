import os
import subprocess
import numpy as np
from itertools import product
import concurrent.futures

# Function to clean directories
def clean_directory(directory):
    import shutil
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Function to perform analysis
def run_analysis(K, link_lat, bw, chunk_size, chunk_per_collective):
    
    # add path to TACOS binary
    TACOS_SRC = '/media/manishdash123/Studies/GaTech_studies/2nd_Sem_Spring_2024/Courses/CS_8803_HW_SW_Codesign_For_ML/research_project/node_traffic_branch/APEX_HML_Project/build/bin/TACOS'
    ROOT_DIR = './apex_outputs'
    OUTPUT_DIR = f'gpu_{K}_link_{link_lat}_bw_{bw}_chunk_{chunk_size}_chunk_coll_{chunk_per_collective}'
    OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_DIR)

    # Ensure the output directory is clean and exists
    if os.path.exists(OUTPUT_PATH):
        clean_directory(OUTPUT_PATH)
    else:
        os.makedirs(OUTPUT_PATH, exist_ok=True)

    command = f"./run_dse.sh {TACOS_SRC} {OUTPUT_PATH} {K} {link_lat} {bw} {chunk_size} {chunk_per_collective}"
    subprocess.run(command, shell=True, check=True)

# Parameters for the product
K = [12] # to be changed for different team members

link_latency = list(range(100, 1000, 100))  # ns
bandwidths = list(range(50, 600, 50))  # GB/s
chunk_size = list(range(1, 4000, 500))  # MB
chunks_per_collective = [1, 2, 4]

param_combinations = list(product(K, link_latency, bandwidths, chunk_size, chunks_per_collective))

# Running the tasks in parallel
def main():
    # Determine the number of cores to use
    total_cores = os.cpu_count()
    number_of_workers = max(8, 12)  # Use all but one core

    # Using ProcessPoolExecutor with a specific number of workers
    with concurrent.futures.ProcessPoolExecutor(max_workers=number_of_workers) as executor:
        # Submit all tasks to the executor
        futures = [executor.submit(run_analysis, *params) for params in param_combinations]

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Get the result of the task
            except Exception as exc:
                print(f'Generated an exception: {exc}')

if __name__ == '__main__':
    main()
