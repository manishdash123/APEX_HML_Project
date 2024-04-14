import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom

def create_separate_tens(height, width, num_timesteps, data_movements):
    graphs = []
    positions = []
    
    # Create independent graphs for each timestep
    for t in range(num_timesteps):
        G = nx.DiGraph()
        pos = {}
        
        # Add nodes and their positions for the current timestep
        for i in range(height):
            for j in range(width):
                node_id = (i, j)
                G.add_node(node_id)
                pos[node_id] = (j, height - i)  # Regular grid positioning

        # Add edges based on chunk movements for the current timestep
        if t < num_timesteps - 1:
            for i in range(height):
                for j in range(width):
                    for (di, dj) in data_movements:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < height and 0 <= nj < width:
                            G.add_edge((i, j), (ni, nj))

        graphs.append(G)
        positions.append(pos)
    
    return graphs, positions

def draw_separate_tens(graphs, positions, width_per_graph=5):
    fig, axes = plt.subplots(1, len(graphs), figsize=(width_per_graph * len(graphs), width_per_graph))
    if len(graphs) == 1:
        axes = [axes]  # ensure axes are iterable
    
    for ax, (G, pos) in zip(axes, zip(graphs, positions)):
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', ax=ax, arrowsize=20, font_size=9)
        ax.set_title(f"Graph at timestep {positions.index(pos)}")

    plt.show()

def preprocess_csv(input_file, output_file):
    timestep_mapping = {}
    current_timestep = 0
    
    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
    
    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        
        for row in rows:
            timestep = float(row[0])
            
            if timestep not in timestep_mapping:
                timestep_mapping[timestep] = current_timestep
                current_timestep += 1
            
            row[0] = str(timestep_mapping[timestep])
            csv_writer.writerow(row)

def draw_graphs(graphs, height, width):
    # Calculate figure size dynamically based on the number of graphs
    fig, axes = plt.subplots(1, len(graphs), figsize=(5 * len(graphs), 5))
    if len(graphs) == 1:
        axes = [axes]  # Make it iterable if only one graph
    
    for i, G in enumerate(graphs):
        ax = axes[i]
        pos = {}  # Dictionary to hold node positions
        
        # Define node positions based on a 2D mesh layout
        for node in G.nodes():
            row = node // width
            col = node % width
            pos[node] = (col, height - 1 - row)  # Invert y-axis to have node 0 at top left
        
        nx.draw(G, pos, with_labels=True, ax=ax, node_size=700, node_color='skyblue', arrows=True, font_size=9)
        
        # Edge labels
        edge_labels = dict(((u, v), d['chunkID']) for u, v, d in G.edges(data=True))
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5, font_size=8, ax=ax)
        
        ax.set_title(f"Timestep {i + 1}")

    plt.tight_layout()
    plt.show()

def preprocess_csv(input_file, output_file):
    """
    Processes the CSV file by mapping each of the timestep values to unique integers.

    Parameters:
    input_file (str): The path to the input CSV file. //Might update with systemn
    output_file (str): The path to the output preprocessed CSV file. //Chage this to store the csv somewhere else

    Returns:
    None
    """
    timestep_mapping = {} # Dictionary to map each timestep to a unique integer
    current_timestep = 0 
    
    with open(input_file, 'r') as file:
        csv_reader = csv.reader(file) # Read the CSV file
        rows = list(csv_reader) # Store the rows of the CSV in a list
    
    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file) # Write to the output CSV file

        #Iterate through each row in the CSV file
        for row in rows:
            timestep = float(row[0]) # Extract the timestep value from the row
            
            if timestep not in timestep_mapping: # If the timestep is not already mapped
                timestep_mapping[timestep] = current_timestep # Map the timestep to the current current_timestep equal 
                current_timestep += 1  # Increment the current_timestep
            
            row[0] = str(timestep_mapping[timestep]) # Update the timestep value in the row
            csv_writer.writerow(row) 



def add_all_nodes(G, height, width):
    """
    Adds all nodes to the graph G.

    Parameters:
    - G (networkx.Graph): The graph to which the nodes will be added.
    - height (int): The height of the grid.
    - width (int): The width of the grid.

    Returns:
    None
    """
    for i in range(height * width):  # Assuming node identifiers are from 0 to height*width-1
        G.add_node(i) #in all the mesh, add nodes

# Get unique timesteps
timesteps = df['Timestep'].unique()

graphs = []

for timestep in timesteps:
    timestep_data = df[df['Timestep'] == timestep] # slice the dataframes into t = 0, 1...N
    print(timestep_data.head)
    
    G = nx.DiGraph() #Create a directed graph
    add_all_nodes(G, height, width)  # Add nodes for this timestep
    
    # Directly use integer identifiers from the CSV
    for _, row in timestep_data.iterrows(): #Iterate through the rows of the dataframe
        source = row['source'] #Extract the source node
        print('src = ',source) 
        destination = row['destination'] #Extract the destination node
        print('dst = ', destination)
        chunkID = row['chunkID']    #Extract the chunkID
        print('chunk = ', chunkID)
        G.add_edge(source, destination, chunkID=chunkID) #Add these nodes as the edge to the graph
    
    graphs.append(G) #Append this graph to the list of graphs

def convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        # Recursively apply to dictionary keys and values
        return {convert_numpy(key): convert_numpy(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        # Apply to each item in the list
        return [convert_numpy(item) for item in obj]
    elif isinstance(obj, tuple):
        # Convert tuple to list (tuples aren't handled in JSON)
        return tuple(convert_numpy(item) for item in obj)
    else:
        return obj


def generate_and_save_xml_pretty(node_traffic, filename):
    root = ET.Element("network")
    for node, edges in node_traffic.items():
        gpu_elem = ET.SubElement(root, "gpu", id=str(node), )
        for destination, records in edges.items():
            tb_elem = ET.SubElement(gpu_elem, "tb", id=str(destination),
                                    send=str(destination if records[0]['type'] == 's' else -1),
                                    recv=str(node if records[0]['type'] == 'r' else -1),
                                    chan ="0")  #Channel fixed to 0
            for record in records:
                ET.SubElement(tb_elem, "step", s=str(record['timestep']), type=record['type'], srcbuf="o", srcoff=str(record['chunkID']), dstbuf="o", dstoff=str(record['chunkID']), cnt="1", depid="-1", deps="-1", hasdep="-1")  #cnt to be changed

    # Convert to string using ElementTree and parse with minidom for pretty print
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    # Write to file
    with open(filename, 'w') as file:
        file.write(pretty_xml_as_string)

# Function to generate and save XML from the node_traffic data
def save_xml_to_file(node_traffic, filename):
    root = ET.Element("network")
    for node, edges in node_traffic.items():
        gpu_elem = ET.SubElement(root, "gpu", id=str(node))
        for destination, records in edges.items():
            tb_elem = ET.SubElement(gpu_elem, "tb", id=str(destination),
                                    send=str(destination if records[0]['type'] == 's' else -1),
                                    recv=str(node if records[0]['type'] == 'r' else -1))
            for record in records:
                if record['type'] == '-1':  # If inactive step
                    ET.SubElement(tb_elem, "step", s=str(record['timestep']), type="-1", chunk="-1")
                else:
                    ET.SubElement(tb_elem, "step", s=str(record['timestep']), type=record['type'], chunk=str(record['chunkID']))

    # Convert the ElementTree to an XML tree and write it to a file
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

# Function to generate XML from the node_traffic data
def generate_xml(node_traffic):
    root = ET.Element("network")
    for node, edges in node_traffic.items():
        gpu_elem = ET.SubElement(root, "gpu", id=str(node))
        for destination, records in edges.items():
            tb_elem = ET.SubElement(gpu_elem, "tb", id=str(destination),
                                    send=str(destination if records[0]['type'] == 's' else -1),
                                    recv=str(node if records[0]['type'] == 'r' else -1))
            for record in records:
                if record['type'] == '-1':  # If inactive step
                    ET.SubElement(tb_elem, "step", s=str(record['timestep']), type="-1", chunk="-1")
                else:
                    ET.SubElement(tb_elem, "step", s=str(record['timestep']), type=record['type'], chunk=str(record['chunkID']))
    return ET.tostring(root, encoding='utf8', method='xml').decode()