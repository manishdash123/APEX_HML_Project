from lxml import etree
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output
import plotly.io as pio
import re

def network_dim(xml_file : str):
    dim = xml_file[4]
    length, width, depth = int(dim), int(dim), int(dim)
    return length, width, depth

class create_topology:
    def __init__(self, xml_file : str):
        self.xml_file = xml_file

    def create_hypercube(self):
        G = nx.DiGraph()
        length, width, depth = network_dim(self.xml_file)
        node_number = 0
        for k in range(depth):  
            for i in range(length):  
                for j in range(width):  
                    new_node = (i, j, k)
                    G.add_node(new_node, label=f"gpu : {node_number}")
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

    def create_torus3d(self):
        G = nx.DiGraph()
        length, width, depth = network_dim(self.xml_file)
        node_number = 0
        for k in range(depth):  
            for i in range(length):  
                for j in range(width):  
                    new_node = (i, j, k)
                    G.add_node(new_node, label=f"gpu : {node_number}")
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

    def create_mesh2D(self):
        G = nx.DiGraph()
        length, width, depth = network_dim(self.xml_file)
        node_number = 0
        for i in range(length):  
            for j in range(width):  
                new_node = (i, j, 0)
                G.add_node(new_node, label=f"gpu : {node_number}")
                node_number += 1

                if (j + 1 < width):
                    G.add_edge(new_node, (i, j + 1, 0))  
                    G.add_edge((i, j + 1, 0), new_node)  

            if (i + 1 < length):
                for j in range(width):
                    G.add_edge(new_node, (i + 1, j, 0))  
                    G.add_edge((i + 1, j, 0), new_node)  

        return G

    def create_torus2D(self):
        G = nx.DiGraph()
        length, width, depth = network_dim(self.xml_file)
        node_number = 0
        for i in range(length):  
            for j in range(width):  
                new_node = (i, j, 0)
                G.add_node(new_node, label=f"gpu : {node_number}")
                node_number += 1

                next_j = (j+1) % width
                G.add_edge(new_node, (i, next_j, 0))  
                G.add_edge((i, next_j, 0), new_node)  

            next_i = (i+1) % length
            for j in range(width):
                G.add_edge(new_node, (next_i, j, 0))  
                G.add_edge((next_i, j, 0), new_node)  

        return G

class visualizer:    
    def __init__(self, topology : str, xml_file : str):
        self.topology = topology
        self.xml_file = xml_file
        self.timestep_data = self.parse_xml()
        self.current_timestep = 0
        self.max_timestep = len(self.timestep_data) - 1

        with open('plot_viewer.html') as file:
            html_content = file.read()

        updated_html_content = re.sub(
            r'const maxTimestep\s*=\s*\d+;',  # Regex to match the line
            f'const maxTimestep = {self.max_timestep};',  # Replacement string
            html_content
        )

        with open('plot_viewer.html', "w") as file:
            file.write(updated_html_content)

        self.update_plot()

    def parse_xml(self):
        tree = etree.parse(self.xml_file)
        root = tree.getroot()
        timestep_data = {}

        for gpu in root.findall("gpu"):
            gpu_id = gpu.get("id")
            for tb in gpu.findall("tb"):
                tb_id = tb.get("id") #thread block ID
                tb_gpuid_send = tb.get("send") #send threadblock ID
                tb_gpuid_recv = tb.get("recv") #Receive threadblock ID
                for step in tb.findall("step"):
                    step_id = step.get("s") #step ID number
                    pkt_type = step.get("type") #send or receive packet?
                    has_dep = step.get("has_dep") #has dependency? A boolean
                    depid = step.get("depid") #dependent thread block ID
                    deps = step.get("deps") #dependent step for the corresponding thread block
                    chunk_id = step.get("srcoff") #chunk id

                    if step_id not in timestep_data:
                        timestep_data[step_id] = {gpu_id : {tb_id : {"pkt_type" : pkt_type, "tb_gpuid_send" : tb_gpuid_send, "tb_gpuid_recv" :tb_gpuid_recv, "chunk_id" : chunk_id}}}
                    else:
                        if gpu_id not in timestep_data[step_id]:
                            timestep_data[step_id][gpu_id] = {tb_id : {"pkt_type" : pkt_type, "tb_gpuid_send" : tb_gpuid_send, "tb_gpuid_recv" :tb_gpuid_recv, "chunk_id" : chunk_id}}
                        else:
                            if tb_id not in timestep_data[step_id][gpu_id]:
                                timestep_data[step_id][gpu_id][tb_id] = {"pkt_type" : pkt_type, "tb_gpuid_send" : tb_gpuid_send, "tb_gpuid_recv" :tb_gpuid_recv, "chunk_id" : chunk_id}
        return timestep_data

    def create_curve(self, start, end, height_factor=0.2):
        """Create a curved path between two points."""
        curve = None
        mid = (start + end) / 2
        t = np.linspace(0, 1, 50)

        if (self.topology == "Mesh2D"):
            if (start[1] == end[1]):
                mid[1] += np.linalg.norm(end - start) * height_factor
            else:
                mid[0] += np.linalg.norm(end - start) * height_factor
            curve = np.outer(1-t, start) + np.outer(t, end) + np.outer(4*t*(1-t), mid-0.5*(start+end))

        elif (self.topology == "Torus2D"):
            if (start[1] == end[1]):
                if (abs(start[0] - end[0]) > 1):
                    mid[2] += np.linalg.norm(end - start) * height_factor
                else:    
                    mid[1] += np.linalg.norm(end - start) * height_factor
            else:
                if (abs(start[1] - end[1]) > 1):
                    mid[2] += np.linalg.norm(end - start) * height_factor
                else:    
                    mid[0] += np.linalg.norm(end - start) * height_factor
            curve = np.outer(1-t, start) + np.outer(t, end) + np.outer(4*t*(1-t), mid-0.5*(start+end))

        elif (self.topology == "Hypercube3D"):
            if (start[2] == end[2]):
                mid[2] += np.linalg.norm(end - start) * height_factor
            else:
                mid[0] += np.linalg.norm(end - start) * height_factor
            curve = np.outer(1-t, start) + np.outer(t, end) + np.outer(4*t*(1-t), mid-0.5*(start+end))
        
        elif (self.topology == "Torus3D"):
            if (start[2] == end[2]):
                if (start[1] == end[1]):
                    mid[2] += np.linalg.norm(end - start) * height_factor * abs(end[0] - start[0])
                else:
                    mid[2] += np.linalg.norm(end - start) * height_factor
            else:
                mid[0] += np.linalg.norm(end - start) * height_factor * abs(end[2] - start[2])
            curve = np.outer(1-t, start) + np.outer(t, end) + np.outer(4*t*(1-t), mid-0.5*(start+end))
        
        return curve

    # Function to create scatter plot for nodes and edges per timestep
    def update_plot(self):
        for i in range(self.max_timestep + 1):
            #Create topology
            topology = create_topology(self.xml_file)
        
            if (self.topology == "Mesh2D"):
                G = topology.create_mesh2D()
            elif (self.topology == "Torus2D"):
                G = topology.create_torus2D()
            elif (self.topology == "Hypercube3D"):
                G = topology.create_hypercube()
            elif (self.topology == "Torus3D"):
                G = topology.create_torus3d()

            length, width, depth = network_dim(self.xml_file)
            nodes = np.array(G.nodes())

            time_data = self.timestep_data[f'{self.current_timestep}']
        
            # Nodes scatter plot
            scatter = go.Scatter3d(
                x=nodes[:, 0], y=nodes[:, 1], z=nodes[:, 2],
                mode='markers',
                marker=dict(size=12, color='blue'),
                hoverinfo='text',
                hovertext=[f"gpu : {gpu_id}" for gpu_id in range(length * width * depth)]
            )
            
            # Edges and arrows
            edges = []
            for gpu_id, gpu_data in time_data.items():
                for tb_id, tb_data in gpu_data.items():
                    if (tb_data['pkt_type'] == 's'):
                        edges.append((int(gpu_id), int(tb_data['tb_gpuid_send']), int(tb_data['chunk_id'])))
                    elif (tb_data['pkt_type'] == 'r'):
                        edges.append((int(tb_data['tb_gpuid_recv']), int(gpu_id), int(tb_data['chunk_id'])))
            
            arrows = []
            x = []
            edges = list(set(edges))

            for edge in edges:
                start_node = nodes[edge[0]]
                end_node = nodes[edge[1]]
                chunk_id = edge[2]

                # Convert start_node and end_node to tuples for comparison
                start_node_tuple = tuple(start_node)
                end_node_tuple = tuple(end_node)
                
                """
                    for example if an edge is ((0,0,0), (0,0,1)), it doesn't exist in x, so append it to x, and draw a curved line and 
                    arrow from edge 0 to edge 1 with arrow pointing towards edge 1
                    
                    if ((0,0,1),(0,0,0)) appears, check if ((0,0,0),(0,0,1)) i.e., reverse of this exists in the list. If so remove this 
                    entry from the list and draw a curved line and arrow from edge 1 to edge 0, with arrow pointing towards edge 0
                """

                if (end_node_tuple, start_node_tuple) in x:
                    curve = self.create_curve(start_node, end_node, -0.05)
                    x.remove((end_node_tuple, start_node_tuple))
                else:
                    x.append((start_node_tuple, end_node_tuple))
                    curve = self.create_curve(start_node, end_node, 0.05)

                line = go.Scatter3d(
                    x=curve[:, 0], y=curve[:, 1], z=curve[:, 2],
                    mode='lines',
                    line=dict(color='black', width=2),
                    hoverinfo='text',
                    hovertext=f"Chunk_id : {chunk_id}"
                )
                
                arrows.append(line)
                tangent = curve[-1] - curve[-7]

                arrow = go.Cone(
                    x=[end_node[0]], y=[end_node[1]], z=[end_node[2]],
                    u=[tangent[0]], 
                    v=[tangent[1]], 
                    w=[tangent[2]],
                    sizemode="absolute",
                    sizeref=0.1,  # Adjust the size reference to control arrow size
                    anchor="tip",
                    showscale=False,
                    colorscale="Viridis"  # You can change the color as needed
                )

                arrows.append(arrow)
                
            # 3D Plot Layout
            layout = go.Layout(
                title=f"Time step = {self.current_timestep}",
                scene=dict(
                    xaxis=dict(showgrid=True, showticklabels=False, title = ""),
                    yaxis=dict(showgrid=True, showticklabels=False, title = ""),
                    zaxis=dict(showgrid=True, showticklabels=False, title = "")
                ),
                showlegend=False
            )

            fig = go.Figure(data=[scatter] + arrows, layout=layout)
            pio.write_html(fig, f'timestep_{self.current_timestep}.html')

            self.current_timestep += 1