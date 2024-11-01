import networkx as nx
import matplotlib.pyplot as plt
import math
import csv
import plotly.graph_objects as go
import os

# Load flow data from CSV file
flow_data = []
xmlfile = "gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.csv"

with open(xmlfile, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        for i in range(len(row)):
            row[i] = int(row[i])
        flow_data.append(row)

def network_dim():
    dim = xmlfile[4]
    length, width, depth = int(dim), int(dim), int(dim)
    return length, width, depth

class create_topology:
    def __init__():
        pass

    def create_hypercube():
        G = nx.DiGraph()
        length, width, depth = network_dim()
        node_number = 0
        for k in range(depth):  
            for i in range(length):  
                for j in range(width):  
                    new_node = (i, j, k)
                    G.add_node(new_node, label=f"{node_number}")
                    node_number += 1

                    if (j + 1 < width):
                        G.add_edge(new_node, (i, j + 1, k))  
                        G.add_edge((i, j + 1, k), new_node)  

                if (i + 1 < length):
                    for j in range(width):
                        G.add_edge(new_node, (i + 1, j, k))  
                        G.add_edge((i + 1, j, k), new_node)  

            if (k + 1 < depth):
                for i in range(length):
                    for j in range(width):
                        G.add_edge(new_node, (i, j, k + 1))  
                        G.add_edge((i, j, k + 1), new_node)  
        return G

    def create_torus3d():
        G = nx.DiGraph()
        length, width, depth = network_dim()
        node_number = 0
        for k in range(depth):  
            for i in range(length):  
                for j in range(width):  
                    new_node = (i, j, k)
                    G.add_node(new_node, label=f"{node_number}")
                    node_number += 1

                    next_j = (j+1) % width
                    G.add_edge(new_node, (i, next_j, k))  
                    G.add_edge((i, next_j, k), new_node)

                next_i = (i+1) % length
                for j in range(width):
                    G.add_edge(new_node, (next_i, j, k))  
                    G.add_edge((next_i, j, k), new_node) 

            next_k = (k+1) % depth
            for i in range(length):
                for j in range(width):
                    G.add_edge(new_node, (i, j, next_k))  
                    G.add_edge((i, j, next_k), new_node)  
        return G

    def create_mesh2D():
        G = nx.DiGraph()
        length, width, depth = network_dim()
        node_number = 0
        for i in range(length):  
            for j in range(width):  
                new_node = (i, j, 0)
                G.add_node(new_node, label=f"{node_number}")
                node_number += 1

                if (j + 1 < width):
                    G.add_edge(new_node, (i, j + 1, 0))  
                    G.add_edge((i, j + 1, 0), new_node)  

            if (i + 1 < length):
                for j in range(width):
                    G.add_edge(new_node, (i + 1, j, 0))  
                    G.add_edge((i + 1, j, 0), new_node)  

        return G

    def create_torus2D():
        G = nx.DiGraph()
        length, width, depth = network_dim()
        node_number = 0
        for i in range(length):  
            for j in range(width):  
                new_node = (i, j, 0)
                G.add_node(new_node, label=f"{node_number}")
                node_number += 1

                next_j = (j+1) % width
                G.add_edge(new_node, (i, next_j, 0))  
                G.add_edge((i, next_j, 0), new_node)  

            next_i = (i+1) % length
            for j in range(width):
                G.add_edge(new_node, (next_i, j, 0))  
                G.add_edge((next_i, j, 0), new_node)  

        return G
    
class TENVisualizer:
    def __init__(self, topo : str):
        self.topology_type = topology

        if topo == "Mesh2D" or topo == "Torus2D":
            num_nodes = int(xmlfile[4]) * int(xmlfile[4])
        elif topo == "Hypercube3D" or topo == "Torus3D":
            num_nodes = int(xmlfile[4]) * int(xmlfile[4]) * int(xmlfile[4])

        self.G, self.time_steps = self.build_time_expanded_network(flow_data, num_nodes)
        self.num_nodes = num_nodes
        self.current_time_step = 0
        
        # Create output directory for HTML files
        self.output_dir = "TENS_plots"
        os.makedirs(self.output_dir, exist_ok=True)

        # Draw the initial step
        self.exportAllStepsasPNG()

    def build_time_expanded_network(self, flow_data, num_nodes):
        time_steps = sorted(set(t for t, _, _, _ in flow_data))
        G = nx.DiGraph()

        topology = create_topology

        if self.topology_type == "Mesh2D":
            G_ = topology.create_mesh2D()
        elif self.topology_type == "Torus2D":
            G_ = topology.create_torus2D()
        elif self.topology_type == "Hypercube3D":
            G_ = topology.create_hypercube()
        elif self.topology_type == "Torus3D":
            G_ = topology.create_torus3d()

        mesh_edges = []
        for edge in G_.edges():
            x_, y_ = None, None
            for node in G_.nodes(data=True):
                if (edge[0] == node[0]):
                    x_ = int(node[1]['label'])
                elif (edge[1] == node[0]):
                    y_ = int(node[1]['label'])
            mesh_edges.append((x_, y_))

        # Add nodes and dashed edges for the entire time-expanded network
        for t in time_steps + [max(time_steps) + 1]:
            for n in range(num_nodes):
                G.add_node(f"{n}_{t}", node=n, time=t)

            # Add dashed edges for the mesh topology at each time step
            if t < max(time_steps) + 1:
                for src, dst in mesh_edges:
                    G.add_edge(f"{src}_{t}", f"{dst}_{t+1}", hold=True)
                    G.add_edge(f"{dst}_{t}", f"{src}_{t+1}", hold=True)

        # Add edges based on flow_data as solid lines for transmitted data
        for t, chunk_id, src, dst in flow_data:
            G.add_edge(f"{src}_{t}", f"{dst}_{t+1}", chunk=chunk_id)

        return G, time_steps

    def draw_time_expanded_network(self, G, current_time_step, num_nodes):
        # Create figure
        fig = plt.figure(figsize=(12, 8))

        # Set positions: Time on x-axis, Node ID on y-axis
        pos = {}
        side_length = int(math.sqrt(num_nodes))
        
        for node in G.nodes():
            n, t = map(int, node.split('_'))
            row, col = divmod(n, side_length)
            pos[node] = (t, side_length * row + col)  # Adjust the y-position based on row and col

        # Draw nodes
        plt.clf()  # Clear the previous plot if there is one
        plt.title(f"Time-Expanded Network Visualization for {self.topology_type} Topology - Time Step: {current_time_step}")
        
        nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue', node_shape='s')

        # Draw node labels (node IDs)
        node_labels = {node: node.split('_')[0] for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

        # Separate edges based on style for the current transition
        edges = G.edges(data=True)
        
        # Draw all mesh connections as dashed lines
        dashed_edges = [(u, v) for u, v, data in edges if 'hold' in data]
        nx.draw_networkx_edges(
            G, pos, edgelist=dashed_edges, edge_color='gray', style='dashed', arrows=False
        )
        
        # Draw chunk movement edges as solid red only for the current time step
        chunk_edges = [
            (u, v) for u, v, data in edges 
            if 'chunk' in data and u.split('_')[1] == str(current_time_step)
        ]
        nx.draw_networkx_edges(
            G, pos, edgelist=chunk_edges, edge_color='red', style='solid', arrows=True
        )

        # Draw edge labels for chunk movement edges
        edge_labels = {
            (u, v): f"{data['chunk']}" for u, v, data in edges if 'chunk' in data and u.split('_')[1] == str(current_time_step)
        }
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue', font_size=6, label_pos=0.25)

        plt.xlabel('Time Step')
        plt.ylabel('Node')
        plt.grid(True)
        plt.axis('on')
        plt.draw()

        return fig  # Return the figure object

    def exportAllStepsasPNG(self):
        for i in range(len(self.time_steps)):
            fig = self.draw_time_expanded_network(self.G, self.current_time_step, self.num_nodes)
            
            # Save the plot as a PNG file
            output_path = os.path.join(self.output_dir, f"timestep_{self.current_time_step}.png")

            fig.savefig(f'{output_path}')
            
            self.current_time_step += 1

# Example usage
topology = "Torus3D"
visualizer = TENVisualizer(topology)