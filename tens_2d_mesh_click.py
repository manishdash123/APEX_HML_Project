import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import math

# Format: (timestep, data ID, source, target)
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

def get_2d_mesh_edges(nodes):
    """Returns edges for a 2D mesh topology based on the number of nodes."""
    side_length = int(math.sqrt(nodes))
    edges = []
    
    for i in range(nodes):
        row, col = divmod(i, side_length)
        
        # Add edge to the right neighbor
        if col < side_length - 1:
            edges.append((i, i + 1))
        # Add edge to the bottom neighbor
        if row < side_length - 1:
            edges.append((i, i + side_length))
    
    return edges

def build_time_expanded_network(flow_data, num_nodes):
    time_steps = sorted(set(t for t, _, _, _ in flow_data))
    G = nx.DiGraph()

    # Determine the mesh edges
    mesh_edges = get_2d_mesh_edges(num_nodes)

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

def draw_time_expanded_network(G, current_time_step, num_nodes):
    # Set positions: Time on x-axis, Node ID on y-axis
    pos = {}
    side_length = int(math.sqrt(num_nodes))
    
    for node in G.nodes():
        n, t = map(int, node.split('_'))
        row, col = divmod(n, side_length)
        pos[node] = (t, side_length * row + col)  # Adjust the y-position based on row and col

    # Draw nodes
    plt.clf()  # Clear the previous plot
    plt.title(f"Time-Expanded Network Visualization for 2D Mesh Topology - Time Step: {current_time_step}")
    
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
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue', font_size=6, label_pos=0.9)

    plt.xlabel('Time Step')
    plt.ylabel('Node')
    plt.grid(True)
    plt.axis('on')
    plt.draw()  # Redraw the plot

class TENVisualizer:
    def __init__(self, G, time_steps, num_nodes):
        self.G = G
        self.time_steps = time_steps
        self.num_nodes = num_nodes
        self.current_time_step = 0

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)

        # Create next and previous buttons
        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.bnext = Button(axnext, 'Next')
        self.bprev = Button(axprev, 'Previous')
        self.bnext.on_clicked(self.next_step)
        self.bprev.on_clicked(self.prev_step)

        self.draw_current_step()

    def draw_current_step(self):
        draw_time_expanded_network(self.G, self.current_time_step, self.num_nodes)
        plt.draw()

    def next_step(self, event):
        if self.current_time_step < max(self.time_steps):
            self.current_time_step += 1
        self.draw_current_step()

    def prev_step(self, event):
        if self.current_time_step > 0:
            self.current_time_step -= 1
        self.draw_current_step()

# Example usage
num_nodes = 9  # Example for a 3x3 mesh
G, time_steps = build_time_expanded_network(flow_data, num_nodes)
visualizer = TENVisualizer(G, time_steps, num_nodes)
plt.show()
