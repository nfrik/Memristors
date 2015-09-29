__author__ = 'nfrik'

import networkx as nx;
import matplotlib.pylab as plt;
import random
import pygraphviz as pgv;


G=nx.random_regular_graph(3,10)


for e in G.edges_iter():
    rval=round(random.random()*10,2);
    G[e[0]][e[1]]['weight']=rval;
    # edge_labels[e]=rval;

# edge_labels=dict([((u,v,),str(d['weight'])) for u,v,d in G.edges(data=True)])
edge_labels=nx.get_edge_attributes(G,'weight')

fig,ax = plt.subplots()

nx.draw(G,ax=ax)
nx.draw_networkx_edge_labels(G,pos=nx.spring_layout(G),labels=edge_labels,font_size=5,ax=ax)

plt.savefig('show.png')
# plt.show()
