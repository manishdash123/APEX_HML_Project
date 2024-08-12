import json
import argparse
import csv
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import os
import pprint
import matplotlib.image as mpimg
from networkx.drawing.nx_agraph import to_agraph
import time

#Function for parsing the python command.
def setup_parser():
    parser = argparse.ArgumentParser(description="Run experiments with specified parameters.")
    parser.add_argument('--K', type=int, default=3, help='Parameter K')
    parser.add_argument('--link_lat', type=int, default=500, help='Link latency')
    parser.add_argument('--bw', type=int, default=50, help='Bandwidth')
    parser.add_argument('--chunk_size', type=int, default=1024, help='Chunk size')
    parser.add_argument('--chunk_per_collective', default=1, type=int, help='Chunks per collective')
    parser.add_argument('--debug', default=False, type=int, help='DEBUG MODE')
    parser.add_argument('--topology_dimensions', default=True, type=int, help='No. of Dimensions for the particular topology. Ex : 2D (or) 3D')
    return parser

#Preprocess CSV using Pandas library. (Just modified the timestep values)
def preprocess_csv(input_file, output_file):
    
    # x = time.time()
    
    df = pd.read_csv(input_file, header=None)
    unique_timesteps = df.iloc[:,0].unique()
    timestep_mapping = {original: new for new, original in enumerate(unique_timesteps)}
    df.iloc[:,0] = df.iloc[:,0].map(timestep_mapping)
    df.to_csv(output_file, index=False, header=False)
    
    # y = time.time()
    
    # print(f"Preprocess CSV function time taken : {y - x} seconds")
  
#Using a single time step, create the data structure.      
def create_data_structure(node_traffic, first_graph, graphs, debug):
    
    # x = time.time()
    
    for node in first_graph.nodes():
        
        node_traffic[node] = {}
        edge_counter = 0  # Reset counter for each node

        # Add thread blocks for all outgoing edges
        for target in first_graph.successors(node):
            node_traffic[node][(node, target)] = {
                'threadID': edge_counter,
                'records': [{'timestep': t, 'chunkID': -1, 'type': '-1', 'depid': -1, 'deps': -1, 'hasdep': 0} for t in graphs.keys()]
            }
            edge_counter += 1

        # Add thread blocks for all incoming edges if not already added
        for source in first_graph.predecessors(node):
            if (source, node) not in node_traffic[node]:
                node_traffic[node][(source, node)] = {
                    'threadID': edge_counter,
                    'records': [{'timestep': t, 'chunkID': -1, 'type': '-1', 'depid': -1, 'deps': -1, 'hasdep': 0} for t in graphs.keys()]
                }
                edge_counter += 1

    # Populate the node_traffic with actual data from all timestep graphs
    for t_index, graph in graphs.items():
        for source, destination, data in graph.edges(data=True):
            node_traffic[source][(source, destination)]['records'][t_index]['chunkID'] = data['label']
            node_traffic[source][(source, destination)]['records'][t_index]['type'] = 's'
            node_traffic[destination][(source, destination)]['records'][t_index]['chunkID'] = data['label']
            node_traffic[destination][(source, destination)]['records'][t_index]['type'] = 'r'

    # Reassign Timesteps ------> Ignore negatives
    for gpu, threadblocks in sorted(node_traffic.items()):
            
        # Create <tb> tags for each connected edge
        for (source, destination), timesteps in threadblocks.items():

            step_counter = 0
            
            # iterate over the list of timesteps
            for step in timesteps['records']:
                
                if step['type'] == '-1':
                    step['timestep'] = "-1"
                    continue
                
                step['timestep'] = step_counter
                step_counter += 1
                
    # y = time.time()
    
    print(f"Create data structure function time taken : {y - x} seconds")
                
# Function to generate and save XML in a pretty format
def generate_and_save_xml_pretty(node_traffic, filename, chunks_per_collective, num_npus, num_timesteps):
    # count = 0
    
    # x = time.time()
    
    root = ET.Element("algo", name = "allgather_ring_1channelsperring", proto="LL128", nchannels="1", nchunksperloop=str(chunks_per_collective), ngpus=str(num_npus), coll="allgather", inplace="1", maxcount="1", nthreadblocks="1")

    # df = pd.DataFrame(node_traffic)
    
    # Create <gpu> tags for each node
    for node, edges in sorted(node_traffic.items()):
        gpu_elem = ET.SubElement(root, "gpu", 
                                 id=str(node), 
                                 i_chunks="0", 
                                 o_chunks=str(num_npus), 
                                 s_chunks="0")

        # Create <tb> tags for each connected edge
        for (source, destination), edge_info in edges.items():
            tb_elem = ET.SubElement(gpu_elem, "tb", 
                                    id=str(edge_info['threadID']),
                                    send=str(destination if edge_info['records'][0]['type'] == 's' else '-1'),
                                    recv=str(source if edge_info['records'][0]['type'] == 'r' else '-1'),
                                    chan="0")
            
            # src = [df[source][(source, destination)]['records'][timestep]['type'] == 's' for timestep in range(num_timesteps)]
            # dst = [df[destination][(source, destination)]['records'][timestep]['type'] == 'r' for timestep in range(num_timesteps)]
            
            # create <step> tags for each time step
            for record in edge_info['records']:
                # print(record['timestep'])
                
                if record['type'] == '-1':
                    continue
                
                # chunkID = df[node][(source, destination)]['records'][record['timestep']]['chunkID']
                # ax = any(df[node][(source, destination)]['records'][timestep]['chunkID'] == chunkID for timestep in range(num_timesteps))
                # print("ChunkID \n" , chunkID)
                # print()
                # print("src \n", ax and src)
                # print()
                # print("dst \n", ax and dst)
                # print()
                
                # xt = time.time()
                
                # Check for matching chunkID between 's' and 'r' records
                # Check other thread blocks   
                for (source_other, destination_other), edge_info_other in edges.items():
                    # for the other thread blocks, check the step
                    for record_other in edge_info_other['records']:
                        if(record['type'] == 's' and record_other['type'] == 'r'):
                            if(record['chunkID'] == record_other['chunkID']):  
                                record['hasdep'] = 1
                                record['depid'] = edge_info_other["threadID"]
                                record['deps'] = record_other['timestep']
         
                yt = time.time()
                
                # print(f"Time taken for checking dependencies for node {node}, {edge_info['threadID']} is {yt - xt} seconds")
                # diff = yt - xt
                # count += diff
                
                # if record['type'] != '-1':
                ET.SubElement(tb_elem, "step", 
                              s=str(record['timestep']), 
                              type=record['type'], 
                              srcbuf="o",
                              srcoff=str(record['chunkID']), #Chunk ID
                              dstbuf="o", 
                              dstoff=str(record['chunkID']),
                              cnt=str(chunks_per_collective), #cnt = chunks per collective
                              depid=str(record['depid']),  #depid = Dependent GPU ID
                              deps=str(record['deps']), #deps = dependent time step
                              hasdep=str(record['hasdep'])) #hasdep = Has dependency?
    
    # print(f"Total time : {count} seconds")
    # Convert to string using ElementTree and parse with minidom for pretty printing
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    # Write to file
    with open(filename, 'w') as file:
        file.write(pretty_xml_as_string)
        
    # y = time.time()
    
    # print(f"Generate XML function time taken : {y - x} seconds")
                
def main():

    parser = setup_parser()
    args = parser.parse_args()

    mesh_dim = args.K
    link_lat = args.link_lat
    bw = args.bw
    chunk_size = args.chunk_size
    chunks_per_collective = args.chunk_per_collective
    debug = args.debug
    dimensions = args.topology_dimensions

    # Number of NPUs = mesh dimensions raised to the power of dimensions.
    num_npus = int(mesh_dim ** dimensions)
    
    npu_ids = range(num_npus)

    # input and output CSV file paths
    tacos_input_file = 'build/bin/output.csv'
    file_name_prefix = f'gpu_{mesh_dim}_link_{link_lat}_bw_{bw}_chunk_{chunk_size}_chunk_coll_{chunks_per_collective}_dimensions_{dimensions}'
    tacos_preprocessed_output_file = f'{file_name_prefix}.csv'

    # <---------------------------------------------------------- STEP 1: PREPROCESS OUTPUT.CSV --------------------------------------------------------->

    # Preprocess the CSV file
    preprocess_csv(tacos_input_file, tacos_preprocessed_output_file)

    # <---------------------------------------------------------- STEP 2: CREATE GRAPHS --------------------------------------------------------->

    df = pd.read_csv(tacos_preprocessed_output_file, header=None) #Header row doesn't exists
    df.columns = ['Timestep', 'chunkID', 'source', 'destination']

    # Create graphs per timestep
    graphs = {t: nx.DiGraph() for t in df['Timestep'].unique()}

    # add all gpu_ids to all the graphs per time step.
    for t, graph in graphs.items():
        graph.add_nodes_from(npu_ids)

    # Populate each graph
    for _, row in df.iterrows():
        graphs[row['Timestep']].add_edge(row['source'], row['destination'], label=row['chunkID'])

    # <---------------------------------------------------------- STEP 3: CREATE DATA STRUCTURE --------------------------------------------------------->

    # Initialize node_traffic from all possible edges in the first graph
    node_traffic = {}

    first_graph = graphs[0]  # Assuming the first timestep graph is fully representative
    
    create_data_structure(node_traffic=node_traffic, first_graph=first_graph, graphs=graphs, debug=debug)

    # <---------------------------------------------------------- STEP 4: GENERATE XML FILE --------------------------------------------------------->

    # Step 1.4 Generate XML from data structure node_traffic & dump in XML file
    filename = f'{file_name_prefix}.xml'
    generate_and_save_xml_pretty(node_traffic, filename, chunks_per_collective, num_npus, len(df['Timestep'].unique()))
    
    # Read the content of the input XML file
    with open(filename, "r") as file:
        xml_content = file.read()
    
    # Remove the XML declaration
    modified_xml_content = xml_content.replace('<?xml version="1.0" ?>', '').lstrip()
    
    # Write the modified content back to the output file
    with open(filename, "w") as file:
        file.write(modified_xml_content)

if __name__ == "__main__":
    main()