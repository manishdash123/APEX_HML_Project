import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import csv
import time

flow_data = [
    (0, 0, 0, 1), (0, 0, 0, 3), (0, 1, 1, 0), (0, 1, 1, 2), (0, 1, 1, 4),
    (0, 2, 2, 1), (0, 2, 2, 5), (0, 3, 3, 0), (0, 3, 3, 4), (0, 3, 3, 6),
    (0, 4, 4, 1), (0, 4, 4, 3), (0, 4, 4, 5), (0, 4, 4, 7), (0, 5, 5, 2),
    (0, 5, 5, 4), (0, 5, 5, 8), (0, 6, 6, 3), (0, 6, 6, 7), (0, 7, 7, 4),
    (0, 7, 7, 6), (0, 7, 7, 8), (0, 8, 8, 5), (0, 8, 8, 7), (1, 3, 0, 1),
    (1, 1, 0, 3), (1, 4, 1, 0), (1, 0, 1, 2), (1, 0, 1, 4), (1, 5, 2, 1),
    (1, 1, 2, 5), (1, 6, 3, 0), (1, 6, 3, 4), (1, 0, 3, 6), (1, 7, 4, 1),
    (1, 7, 4, 3), (1, 3, 4, 5), (1, 1, 4, 7), (1, 8, 5, 2), (1, 8, 5, 4),
    (1, 4, 5, 8), (1, 3, 6, 7), (1, 4, 7, 6), (1, 6, 7, 8), (1, 7, 8, 5),
    (1, 5, 8, 7), (2, 6, 0, 1), (2, 5, 1, 0), (2, 4, 1, 2), (2, 2, 1, 4),
    (2, 8, 2, 1), (2, 0, 2, 5), (2, 7, 3, 0), (2, 1, 3, 6), (2, 5, 4, 3),
    (2, 6, 4, 5), (2, 0, 4, 7), (2, 7, 5, 2), (2, 3, 5, 8), (2, 8, 7, 6),
    (2, 1, 7, 8), (3, 8, 1, 0), (3, 3, 1, 2), (3, 5, 3, 6), (3, 8, 4, 3),
    (3, 2, 4, 7), (3, 6, 5, 2), (3, 2, 5, 8), (3, 0, 7, 8), (4, 2, 1, 0),
    (4, 2, 4, 3), (4, 2, 7, 6)
]

# with open("gpu_3_link_500_bw_50_chunk_1024_chunk_coll_2.csv", "r") as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         for i in range(len(row)):
#             row[i] = int(row[i])
#         flow_data.append(row)

total_time_steps = sorted(set(t for t, _, _, _ in flow_data))

def visualize_timestep(timestep: int):
    # Extract unique time steps, nodes, and chunk IDs
    time_flow_data = [i for i in flow_data if i[0] == timestep]
    time_steps = sorted(set(t for t, _, _, _ in time_flow_data))
    nodes = sorted(set(n for _, _, n, _ in time_flow_data) | set(n for _, _, _, n in time_flow_data))
    chunk_ids = sorted(set(c for _, c, _, _ in time_flow_data))

    G = nx.DiGraph()

    # Add temporal nodes
    for t in total_time_steps + [max(total_time_steps) + 1]:  # Include the last time step for destinations
        for n in nodes:
            G.add_node(f"{n}_{t}", node=n, time=t)

    # Add edges based on flow_data
    for t, chunk_id, src, dst in time_flow_data:
        G.add_edge(f"{src}_{t}", f"{dst}_{t+1}", chunk=chunk_id)

    # Add holding edges
    for t in time_steps:
        for n in nodes:
            G.add_edge(f"{n}_{t}", f"{n}_{t+1}", hold=True)

    # Set positions: Time on x-axis, Node ID on y-axis
    pos = {}
    for node in G.nodes():
        n, t = node.split('_')
        pos[node] = (int(t), int(n))

    return (G, pos)

def update_plot(current_timestep : int):
    clear_output(wait=True)
    display(prev_button, next_button)
    # Set up the figure once
    plt.figure(figsize=(15, 9))
    
    G, pos = visualize_timestep(current_timestep)
    
    # Clear the current axes instead of the whole figure
    plt.clf()  
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue', node_shape='s')

    # Draw edges
    edges = G.edges(data=True)
    edge_colors = ['red' if 'chunk' in data else 'gray' for _, _, data in edges]
    edge_styles = ['solid' if 'chunk' in data else 'dashed' for _, _, data in edges]

    # Separate edge lists based on style
    chunk_edges = [(u, v) for u, v, data in edges if 'chunk' in data]
    hold_edges = [(u, v) for u, v, data in edges if 'hold' in data]

    # Draw chunk movement edges
    nx.draw_networkx_edges(
        G, pos, edgelist=chunk_edges, edge_color='red', style='solid', arrows=True
    )

    # Draw holding edges
    nx.draw_networkx_edges(
        G, pos, edgelist=hold_edges, edge_color='gray', style='dashed', arrows=False
    )

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8)

    # Annotate edges with chunk IDs
    edge_labels = {}
    for u, v, data in edges:
        if 'chunk' in data:
            edge_labels[(u, v)] = f"{data['chunk']}"
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue', font_size=6, label_pos=0.88)

    # Set plot labels and title
    plt.xlabel('Time Step')
    plt.ylabel('Node')
    plt.title(f'Time-Expanded Network Visualization at Timestep {current_timestep}')
    plt.grid(True)
    plt.show()

# Timestep navigation
current_timestep = 0
max_timestep = len(total_time_steps) - 1

def on_next_button_clicked(b):
    global current_timestep
    if current_timestep < max_timestep:
        print("current_timestep : ", current_timestep)
        current_timestep += 1
        update_plot(current_timestep)

def on_prev_button_clicked(b):
    global current_timestep
    if current_timestep > 0:
        print("current_timestep : ", current_timestep)
        current_timestep -= 1
        update_plot(current_timestep)

# Create Next and Previous buttons
next_button = widgets.Button(description="Next")
prev_button = widgets.Button(description="Previous")

# Bind button clicks to functions
next_button.on_click(on_next_button_clicked)
prev_button.on_click(on_prev_button_clicked)

# Display buttons and initial plot
display(prev_button, next_button)
update_plot(current_timestep)