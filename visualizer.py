from lxml import etree
import networkx as nx
import plotly.graph_objects as go
import numpy as np

timestep_data = {}

tree = etree.parse('gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.xml')

root = tree.getroot()

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

#3D Hypercube visualization
length, width, depth = 2,2,2

def create_hypercube():
    G = nx.DiGraph()
    node_number = 0
    for k in range(depth):  # First, iterate over depth
        for i in range(length):  # Then iterate over rows
            for j in range(width):  # Finally, iterate over columns (within a row)
                new_edge = (i, j, k)
                G.add_node(new_edge, label = f"gpu : {node_number}")
                node_number += 1
                
                # Connect horizontally (within the row)
                if (j + 1 < width):
                    G.add_edge(new_edge, (i, j+1, k))  # send to the right
                    G.add_edge((i, j+1, k), new_edge)  # receive from the right

            # Connect vertically (to the next row in the same depth)
            if (i + 1 < length):
                for j in range(width):  # For each column, connect rows
                    G.add_edge((i, j, k), (i+1, j, k))  # send to the next row
                    G.add_edge((i+1, j, k), (i, j, k))  # receive from the next row

        # After covering all rows and columns for this depth, move to the next depth layer.
        if (k + 1 < depth):
            for i in range(length):
                for j in range(width):
                    G.add_edge((i, j, k), (i, j, k+1))  # send to the next depth
                    G.add_edge((i, j, k+1), (i, j, k))  # receive from the next depth

    return G


for timestep, time_data in timestep_data.items():
    G = create_hypercube()
    
    #Plot all the nodes using plotly
    nodes = np.array(G.nodes())
    scatter = go.Scatter3d(
        x=nodes[:, 0], y=nodes[:, 1], z=nodes[:, 2],
        mode='markers',
        marker=dict(size=10, color='blue'),
        hoverinfo='text',
        hovertext=[f"gpu : {gpu_id}" for gpu_id in range(length * width * depth)]
    )

    #Edge logic
    edges = []
    for gpu_id, gpu_data in time_data.items():
        for tb_id, tb_data in gpu_data.items():
            if (tb_data['pkt_type'] == 's'):
                edges.append((int(gpu_id), int(tb_data['tb_gpuid_send']), int(tb_data['chunk_id'])))
            elif (tb_data['pkt_type'] == 'r'):
                edges.append((int(tb_data['tb_gpuid_recv']), int(gpu_id), int(tb_data['chunk_id'])))
    print(edges)

    arrows = []
    for edge in edges:
        start_node = nodes[edge[0]]
        end_node = nodes[edge[1]]
        chunk_id = edge[2]

        # Line for the arrow shaft
        line = go.Scatter3d(
            x=[start_node[0], end_node[0]],
            y=[start_node[1], end_node[1]],
            z=[start_node[2], end_node[2]],
            mode='lines',
            line=dict(color='red', width=2),
            hoverinfo='text',
            hovertext=f"Chunk_id : {chunk_id}"
        )
        
        # Add an arrowhead as a cone at the end of each edge
        arrow = go.Cone(
            x=[end_node[0]], y=[end_node[1]], z=[end_node[2]], 
            u=[end_node[0] - start_node[0]],  
            v=[end_node[1] - start_node[1]],  
            w=[end_node[2] - start_node[2]],  
            sizemode="absolute",
            sizeref=0.2,  
            anchor="tip", 
            showscale=False,
            colorbar=None,   
            colorscale=None
        )
        
        # Add both the shaft and the arrowhead to the list
        arrows.append(line)
        arrows.append(arrow)

    # Set up the layout for 3D view
    layout = go.Layout(
        scene=dict(
            xaxis=dict(range=[-2, 2], title='X'),
            yaxis=dict(range=[-2, 2], title='Y'),
            zaxis=dict(range=[-2, 2], title='Z'),
            aspectratio=dict(x=1, y=1, z=1)
        )
    )

    # Create the figure with initial frames
    fig = go.Figure(data=[scatter] + arrows, layout=layout)

    fig.show()