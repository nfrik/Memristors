__author__ = 'nfrik'

import networkx as nx;
import matplotlib.pylab as plt;
import random
from ahkab import new_ac, new_op, run
from ahkab.circuit import Circuit
from ahkab.plotting import plot_results

G=nx.random_regular_graph(3,10)


#create circuit
cir = Circuit('Test Current')


for e in G.edges_iter():
    rval=round(random.random()*10,2);
    cir.add_resistor('R'+str(e[0])+str(e[1]),'n'+str(e[0]),'n'+str(e[1]),rval)
    G[e[0]][e[1]]['weight']=rval;
    # edge_labels[e]=rval;


for n in G.nodes_iter():
    G.node[n]['number']=n;

# edge_labels=dict([((u,v,),str(d['weight'])) for u,v,d in G.edges(data=True)])
edge_labels=nx.get_edge_attributes(G,'weight')
node_labels=nx.get_node_attributes(G,'number')

fig,ax = plt.subplots()

pos=nx.spring_layout(G)
nx.draw(G,pos=pos,ax=ax)
nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=edge_labels,font_size=8,ax=ax)
nx.draw_networkx_labels(G,pos=pos,labels=node_labels,font_size=8,ax=ax)

plt.savefig('show.png')
# plt.show()





cir.add_resistor("RG",'n5',cir.gnd,0.001)
cir.add_vsource("V1",'n0',cir.gnd,1);
opa = new_op()
r = run(cir,opa)['op']
print r