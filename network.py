__author__ = 'nfrik'

import networkx as nx;
import matplotlib.pylab as plt;
import random
from ahkab import new_ac, new_op, run
from ahkab.circuit import Circuit
import memristor;

w=0.1
D=1.0
Roff=10.;
Ron=1.;
mu=10.
Tao=0.01

G=nx.random_regular_graph(3,10)

#create circuit
cir = Circuit('Memristor test')

for e in G.edges_iter():
    rval=round(Roff+0.01*Roff*(random.random()-0.5),2);
    cir.add_resistor('R'+str(e[0])+str(e[1]),'n'+str(e[0]),'n'+str(e[1]),rval)
    G[e[0]][e[1]]['weight']=rval;
    # edge_labels[e]=rval;

for n in G.nodes_iter():
    G.node[n]['number']=n;


#Choose randomly ground and voltage terminal nodes
[v1,gnd]=random.sample(xrange(0,len(G.nodes())),2);
lastnode=len(G.nodes());
G.add_edge(v1,lastnode);
G.node[lastnode]['number']='V1';
lastnode+=1;
G.add_edge(gnd,lastnode);
G.node[lastnode]['number']='gnd';


edge_labels=nx.get_edge_attributes(G,'weight')
node_labels=nx.get_node_attributes(G,'number')

fig,ax = plt.subplots()

pos=nx.spring_layout(G)
nx.draw(G,pos=pos,ax=ax)
nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=edge_labels,font_size=8,ax=ax)
nx.draw_networkx_labels(G,pos=pos,labels=node_labels,font_size=8,ax=ax)

plt.savefig('show.png')
# plt.show()



cir.add_resistor("RG",'n'+str(v1),cir.gnd,0.001);
cir.add_vsource("V1",'n'+str(gnd),cir.gnd,1);
opa = new_op();
r = run(cir,opa)['op'];

#Get first voltage values
keys=r.results.keys();
keys.remove('I(V1)'); #for now we know this key


#create memristors list
mems={};
for k in keys:
    curv=r.results[k];
    mems[k]=memristor.memristor(w,D,Roff,Ron,mu,Tao,curv);

#connect

# #evolve the system
# for i in range(1000):
# #update circuit resistor values
#     for k in keys:
#         cir.get_elem_by_name(k).
# #calculate circuit
# #update voltages on memristors
# #save values from memristors

print mems;

print r
