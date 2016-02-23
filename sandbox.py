#learning how to generate networks
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit
import igraph as ig

# #create a graph with degrees following a power law distribution
# s=[]
# while len(s)<100:
#     nextval = int(nx.utils.powerlaw_sequence(1, 2.5)[0]) #100 nodes, power-law exponent 2.5
#     if nextval!=0:
#         s.append(nextval)
# G = nx.configuration_model(s)
# G=nx.Graph(G) # remove parallel edges
# G.remove_edges_from(G.selfloop_edges())
#
# #draw and show graph
# pos = nx.spring_layout(G)
# nx.draw_networkx(G, pos)
# plt.savefig('test.pdf')


def func(x,a,b,c):
    return a*np.exp(-b*x)+c

def powf(x,a,b,c):
    return a*np.power(x,-b)+c

# xdata = np.linspace(0,4,50)
#
# y=func(xdata,2.5,1.3,0.5)
#
# ydata = y+0.2*np.random.normal(size=len(xdata))


# G=nx.barabasi_albert_graph(1000,10)
# G=nx.scale_free_graph(1000)
# z=nx.utils.create_degree_sequence(1000,nx.utils.powerlaw_sequence,exponent=2.1)
# nx.is_valid_degree_sequence(z)
# G=nx.configuration_model(z)
#
# loops=G.selfloop_edges()
# print("graph has {0:d} self-loops".format(len(loops)))
#
# num_par = sum(len(G[node][neigh]) for node in G for neigh in G.neighbors_iter(node))
# print("graph has {0:d} parallel edges".format(num_par))
#
#
# G=nx.Graph(G)
# G.remove_edges_from(loops)

g=ig.Graph.Barabasi(100,power=1.2)
G=nx.Graph(g.get_edgelist())

layout = g.layout("kk")
ig.plot(g)

degree_sequence=sorted(nx.degree(G).values(),reverse=True)
degree_sequence = [float(i)/sum(degree_sequence) for i in degree_sequence]
# fit = np.polyfit(degree_sequence,range(len(degree_sequence)),1)
# print fit
# plt.loglog(degree_sequence,'b-',marker='o')
# plt.show()

xdata = range(1,len(degree_sequence)+1)
# y = powf(xdata,10.,3.,.1)#+0.02*np.random.normal(size=len(xdata))

plt.figure()
pos = nx.spring_layout(G)
# pos = nx.fruchterman_reingold_layout(G)
nx.draw(G, pos)
plt.show()

# plt.plot(xdata,y)
# # plt.loglog(y)
# plt.show()

plt.figure()
popt, pcov = curve_fit(powf,xdata,degree_sequence)
plt.plot(degree_sequence)
plt.plot(powf(xdata,popt[0],popt[1],popt[2]))
# plt.loglog(degree_sequence,'b-',marker='o')
# plt.loglog(powf(xdata,popt[0],popt[1],popt[2]))
plt.show()

#
print popt
print pcov
