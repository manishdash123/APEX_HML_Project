from TensVisualizer import TENVisualizer
from visualizer import visualizer
import csv

topology = "Torus3D"

# Load flow data from CSV file
flow_data = []
csv_file = "gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2_dimensions_3.csv"
xml_file =  "gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2_dimensions_3.xml"

with open(csv_file, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        for i in range(len(row)):
            row[i] = int(row[i])
        flow_data.append(row)

#Run TENS Visualizer
Tens_Viz = TENVisualizer(topology, csv_file, flow_data)

#Run 3D Visualizer
D3_viz = visualizer(topology, xml_file)