import json
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# https://www.idtools.com.au/3d-network-graphs-with-python-and-the-mplot3d-toolkit/

def get_number_of_nodes(graph):
    count = 0
    for child in graph["children"]:
        count += 1
        count += get_number_of_nodes(child)
    return count

def get_maximum_edges(graph):
    count = len(graph["children"])

    for child in graph["children"]:
        count = max(count, get_maximum_edges(child))
        
    return count

def network_plot_3D(graph):
    # Get number of nodes
    n = get_number_of_nodes(graph)

    # Get the maximum number of edges adjacent to a single node
    # edge_max = max([G.degree(i) for i in range(n)])

    # Define color range proportional to number of edges adjacent to a single node
    # colors = [plt.cm.plasma(1) for i in range(n)] 

    # 3D network plot
    with plt.style.context(('ggplot')):
        
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        
        # Loop on the pos dictionary to extract the x,y,z coordinates of each node
        nodes = [graph]
        while len(nodes) != 0:
            node = nodes.pop()

            children = node["children"]
            node = node["node"]

            girth = node["girth"]
            position = node["position"]

            for child in children:
                nodes.append(child)
            
            xi = position[0]
            yi = position[1]
            zi = position[2]

            # Scatter plot
            ax.scatter3D(xi, yi, zi, alpha=0.7)

            # Loop on the list of edges to get the x,y,z, coordinates of the connected nodes
            # Those two points are the extrema of the line to be plotted
            for child in children:
                x = np.array((xi, child["node"]["position"][0]))
                y = np.array((yi, child["node"]["position"][1]))
                z = np.array((zi, child["node"]["position"][2]))
            
                # Plot the connecting lines
                ax.plot3D(x, y, z, c='black', alpha=0.5)
    
    plt.show()
    
    return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: main.py <json file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        graph = json.load(f)

    network_plot_3D(graph)
