import concurrent.futures

# Define the function that will call in parallel
def run_tacos(gpu_mesh, link_bw, bw):
    # ...
    # Save results to output folder as txt and csv
    '''
     K = 25, link = 500, BW = 50, CS=1000
     output_folder = K_25_LINK_500_BW_50_CS_1000
    '''

    # 1. run tacos script ----> produces TACOS_output.txt and output.csv 
    # 2. run analysis script ------> xml
    # 3. run the chakra conversion script -----> ET's
    # 4. run astra-sim -----> pipe to text OR use a python subprocess and make a csv
    pass

# k = [25.....400]

# Create a list of all possible combinations of the variables
gpu_mesh_sizes = [(i, i) for i in range(2, 101)]  # Creates tuples like (2, 2), (3, 3), etc.

# NV: 
link_latency = list(range(500, 10000, 500))  # 200, 300, ..., 1000
bandwidths = list(range(50, 1000, 50))  # 10, 20, ..., 80
chunk_size = list(range(0.001, 10000, 500))

# Generate all combinations of parameters
from itertools import product
param_combinations = list(product(gpu_mesh_sizes, link_latency, bandwidths))

# Function to unpack arguments
def run_with_params(params):
    return run_analysis(*params)

# Run the tasks in parallel using ProcessPoolExecutor
with concurrent.futures.ProcessPoolExecutor() as executor:
    # Map the run_with_params to the list of parameter combinations
    results = list(executor.map(run_with_params, param_combinations))

