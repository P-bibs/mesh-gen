import random
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

def generate_random_3Dgraph(n_nodes, radius, seed=None):

    graph =  {"x": 0, "y": 0, "z": 0, "children": [
            {"x": 0, "y": 0, "z": 0.5, "children": [
                {"x": 0.5, "y": 0, "z": 0.75, "children": []},
                {"x": 0, "y": 0.5, "z": 0.75, "children": []},
                {"x": -0.5, "y": 0, "z": 0.75, "children": []},
                {"x": 0, "y": -0.5, "z": 0.75, "children": []}
        ]},
    ]}

    return graph

def network_plot_3D(graph, angle, save=False):

    
    # Get number of nodes
    n = get_number_of_nodes(graph)

    # Get the maximum number of edges adjacent to a single node
    # edge_max = max([G.degree(i) for i in range(n)])

    # Define color range proportional to number of edges adjacent to a single node
    # colors = [plt.cm.plasma(1) for i in range(n)] 

    # 3D network plot
    with plt.style.context(('ggplot')):
        
        fig = plt.figure(figsize=(10,7))
        ax = Axes3D(fig)
        
        # Loop on the pos dictionary to extract the x,y,z coordinates of each node
        nodes = [graph]
        while len(nodes) != 0:
            node = nodes.pop()
            for child in node["children"]:
                nodes.append(child)
            
            xi = node["x"]
            yi = node["y"]
            zi = node["z"]

            # Scatter plot
            ax.scatter(xi, yi, zi, c=plt.cm.plasma(0.5), edgecolors='k', alpha=0.7)

            # Loop on the list of edges to get the x,y,z, coordinates of the connected nodes
            # Those two points are the extrema of the line to be plotted
            for child in node["children"]:
                x = np.array((xi, child["x"]))
                y = np.array((yi, child["y"]))
                z = np.array((zi, child["z"]))
            
                # Plot the connecting lines
                ax.plot(x, y, z, c='black', alpha=0.5)
    
    # Set the initial view
    ax.view_init(30, angle)

    # Hide the axes
    ax.set_axis_off()

    if save is not False:
        plt.savefig("./data"+str(angle).zfill(3)+".png")
        plt.close('all')
    else:
        plt.show()
    
    return

n=200
G = generate_random_3Dgraph(n_nodes=n, radius=0.25, seed=1)
network_plot_3D(G,0, save=False)

for k in range(20,201,1):

   G = generate_random_3Dgraph(n_nodes=k, radius=0.25, seed=1)

   angle = (k-20)*360/(200-20)
    
   network_plot_3D(G,angle, save=True)

   print(angle)