#!/usr/bin/python3
#!/usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt

# Define the graph dictionary
graph_dict = {
    "Addis Ababa": {
        "Adama": {"distance": 125},
        "Bahir Dar": {"distance": 150},
        "Hawassa": {"distance": 175},
    },
    "Adama": {
        "Addis Ababa": {"distance": 125},
        "Bahir Dar": {"distance": 250},
        "Hawassa": {"distance": 150},  
    },
    "Bahir Dar": {
        "Addis Ababa": {"distance": 150},
        "Adama": {"distance": 250},     
        "Hawassa": {"distance": 200},
    },
    "Hawassa": {
        "Addis Ababa": {"distance": 175},
        "Adama": {"distance": 150},    
        "Bahir Dar": {"distance": 200},
    },
}

# Create an undirected graph
G = nx.Graph()

# Add edges with weights from the dictionary
for source, neighbors in graph_dict.items():
    for target, attrs in neighbors.items():
        G.add_edge(source, target, weight=attrs["distance"])

# Print the graph details (optional)
print("Nodes:", G.nodes())
print("Edges with weights:", G.edges(data=True))

# Visualize the graph
pos = nx.spring_layout(G)  # Position nodes using a spring layout
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Show the plot
plt.title("Graph of Cities with Distances")
plt.show()