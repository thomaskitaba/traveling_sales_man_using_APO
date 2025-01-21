#!/usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt

# Define the road network
roads = {
    "Addis Ababa": {
        "Adama": {"distance": 598, "heuristic": 50},
        "Bahir Dar": {"distance": 225, "heuristic": 150},
        "Hawassa": {"distance": 700, "heuristic": 200},
    },
    "Adama": {
        "Hawassa": {"distance": 164, "heuristic": 150},
        "Addis Ababa": {"distance": 598, "heuristic": 50},
    },
    "Bahir Dar": {
        "Addis Ababa": {"distance": 225, "heuristic": 150},
        "Hawassa": {"distance": 800, "heuristic": 300},
    },
    "Hawassa": {
        "Adama": {"distance": 164, "heuristic": 150},
        "Addis Ababa": {"distance": 700, "heuristic": 200},
    },
}

# Create an empty graph
G = nx.Graph()

# Add nodes and edges with weights
for city, connections in roads.items():
    for destination, attributes in connections.items():
        G.add_edge(city, destination, weight=attributes["distance"])

# Choose a layout for the graph
# Uncomment one of the following layout options:
pos = nx.spring_layout(G)  
# pos = nx.circular_layout(G)  
# pos = nx.kamada_kawai_layout(G)  
# pos = nx.spectral_layout(G)  
# pos = nx.random_layout(G)  
# Draw the graph
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color='lightblue',
    node_size=3100,
    font_size=8,
    font_weight='bold',
    width=2
)

# Draw edge labels (weights)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')

# Display the graph
plt.margins(0.2)
plt.show()
