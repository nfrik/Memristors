import networkx as nx
import matplotlib.pyplot as plt
from random import random


def remove_random_edges(G,alpha=0.0): #alpha = 0:1 - fraction of edges removed
    edges = G.edges();

    for e in edges:
        if random() > (1-alpha):
            G.remove_edge(e[0],e[1])

    return G;

N = 10
G=nx.grid_2d_graph(N,N)
pos = dict( (n, n) for n in G.nodes() )
labels = dict( ((i, j), i + (N-1-j) * 10 ) for i, j in G.nodes() )
G = remove_random_edges(G,0.3)
nx.draw_networkx(G, pos=pos)


print(pos)

plt.axis('off')
plt.show()