__author__ = 'nfrik'
import networkx as nx
import matplotlib.pylab as plt
import random
from ahkab import new_ac, new_op, run
from ahkab.circuit import Circuit
import memristor
import numpy as np
from matplotlib.widgets import Slider


# Get first voltage values
def update_memristor_vals_from_oprun(netdict, r):
    memdict = netdict['Memristors']
    for k in memdict.keys():
        [n0, n1] = ['VN' + str(memdict[k][0]), 'VN' + str(memdict[k][1])]
        [v0, v1] = [r.results[n0], r.results[n1]]
        memdict[k][2].setV(v1 - v0)

    netdict['Memristors'] = memdict
    return netdict


def update_circrvals_from_memres(netdict):
    memdict = netdict['Memristors']
    cir = netdict['Circuit']

    global n
    for k in memdict.keys():
        # memdict[k][2].updateW()
        for n in range(len(cir)):
            if k == cir[n].part_id:
                cir[n].value = memdict[k][2].getR()

    netdict['Memristors'] = memdict
    netdict['Circuit'] = cir
    return netdict


def update_memristor_states(netdict):
    memdict = netdict['Memristors']
    for k in memdict.keys():
        memdict[k][2].updateW()

    netdict['Memristors'] = memdict
    return netdict


def set_cir_voltage(part_id, val, netdict):
    cir = netdict['Circuit']
    for n in range(len(cir)):
        if cir[n].part_id == part_id:
            cir[n].dc_value = val

    netdict['Circuit'] = cir
    return cir


def get_cir_voltage(part_id, netdict):
    cir = netdict['Circuit']
    for n in range(len(cir)):
        if cir[n].part_id == part_id:
            return cir[n].dc_value


def plot_graph(G):
    edge_labels = nx.get_edge_attributes(G, 'weight')
    node_labels = nx.get_node_attributes(G, 'number')

    fig, ax = plt.subplots()
    pos = nx.circular_layout(G)
    nx.draw(G, pos=pos, ax=ax)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_size=8, ax=ax)
    nx.draw_networkx_labels(G, pos=pos, labels=node_labels, font_size=8, ax=ax)

    plt.savefig('show.png')
    plt.close()


def generate_network(mem_pars, net_pars):
    G = nx.random_regular_graph(net_pars['degree'], net_pars['N'])
    cir = Circuit('Memristor network test')

    # assign dictionary with terminals and memristors
    memdict = {}

    w = mem_pars['w']
    D = mem_pars['D']
    Roff = mem_pars['Roff']
    Ron = mem_pars['Ron']
    mu = mem_pars['mu']
    Tao = mem_pars['Tao']

    for e in G.edges_iter():
        rval = round(Roff + 0.01 * Roff * (random.random() - 0.5), 2)
        key = 'R' + str(e[0]) + str(e[1])
        [v1, v2] = [e[0], e[1]]
        memdict[key] = [v1, v2,
                        memristor.memristor(w, D, Roff, Ron, mu, Tao, 0.0)]  # we set v=0.0 value in the beginning
        cir.add_resistor(key, 'n' + str(v1), 'n' + str(v2), rval)
        G[e[0]][e[1]]['weight'] = rval
        # edge_labels[e]=rval;

    for n in G.nodes_iter():
        G.node[n]['number'] = n

    # Choose randomly ground and voltage terminal nodes on graph
    [v1, gnd] = random.sample(xrange(0, len(G.nodes())), 2)
    lastnode = len(G.nodes())
    G.add_edge(v1, lastnode)
    G.node[lastnode]['number'] = 'V1'
    lastnode += 1
    G.add_edge(gnd, lastnode)
    G.node[lastnode]['number'] = 'gnd'

    cir.add_resistor("RG", 'n' + str(gnd), cir.gnd, 0.001)
    cir.add_vsource("V1", 'n' + str(v1), cir.gnd, 1000)
    opa = new_op()

    # netdict contains setup graph and circuit
    netdict = {}
    netdict['Graph'] = G
    netdict['Circuit'] = cir
    netdict['Memristors'] = memdict

    return netdict


w = 0.1
D = 1.0
Roff = 100.
Ron = 1.
mu = 10.
Tao = 0.1

mem_pars = {'w': w, 'D': D, 'Roff': Roff, 'Ron': Ron, 'mu': mu, 'Tao': Tao}

net_pars = {'degree': 3, 'N': 10}

netdict = generate_network(mem_pars, net_pars)

global a0, f0
a0 = 1000
f0 = 10

# cir = Circuit('Memristor test')
# G=nx.random_regular_graph(3,10)
#
# #create circuit
#
# #assign dictionary with terminals and memristors
# memdict={}
# for e in G.edges_iter():
#     rval=round(Roff+0.01*Roff*(random.random()-0.5),2)
#     key='R'+str(e[0])+str(e[1])
#     [v1,v2]=[e[0],e[1]]
#     memdict[key]=[v1,v2,memristor.memristor(w,D,Roff,Ron,mu,Tao,0.0)] # we set v=0.0 value in the beginning
#     cir.add_resistor(key,'n'+str(v1),'n'+str(v2),rval)
#     G[e[0]][e[1]]['weight']=rval
#     # edge_labels[e]=rval;
#
# for n in G.nodes_iter():
#     G.node[n]['number']=n
#
#
# #Choose randomly ground and voltage terminal nodes on graph
# [v1,gnd]=random.sample(xrange(0,len(G.nodes())),2)
# lastnode=len(G.nodes())
# G.add_edge(v1,lastnode)
# G.node[lastnode]['number']='V1'
# lastnode+=1
# G.add_edge(gnd,lastnode)
# G.node[lastnode]['number']='gnd'
#
# edge_labels=nx.get_edge_attributes(G,'weight')
# node_labels=nx.get_node_attributes(G,'number')
#
# fig,ax = plt.subplots()
# pos=nx.circular_layout(G)
# nx.draw(G,pos=pos,ax=ax)
# nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=edge_labels,font_size=8,ax=ax)
# nx.draw_networkx_labels(G,pos=pos,labels=node_labels,font_size=8,ax=ax)
#
# plt.savefig('show.png')
# plt.close()
# #plt.show()

# cir.add_resistor("RG",'n'+str(gnd),cir.gnd,0.001)
# cir.add_vsource("V1",'n'+str(v1),cir.gnd,1000)
# opa = new_op()

# get initial voltages
# set_mem_voltages(r);

# memdict_t={}



circ_state = []
x = 0
y = 0
fig = plt.figure(1)
ax = fig.add_subplot(211)
ax1 = fig.add_subplot(212)
plt.subplots_adjust(left=0.25, bottom=0.25)

r = run(cir, opa)['op']
line = [None] * (len(r.results.keys()))
for n in range(len(line)):
    line[n], = ax.plot(x, y)

l2, = ax1.plot(x, y)

axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
axamp = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

sfreq = Slider(axfreq, 'Freq', 0.01, 20.0, valinit=f0)
samp = Slider(axamp, 'Amp', 0.1, 1500.0, valinit=a0)


def update(val):
    a0 = samp.val
    f0 = sfreq.val


sfreq.on_changed(update)
samp.on_changed(update)

for i in range(10000):
    r = run(cir, opa)['op']
    update_memristor_vals_from_oprun(r)
    update_memristor_states()
    update_circrvals_from_memres()
    circ_state.append(r)

    for p in range(len(r.results.keys()) - 1):
        x = np.concatenate((line[p].get_xdata(), [i]))
        y = np.concatenate((line[p].get_ydata(), [r.results['VN' + str(p)]]))
        line[p].set_data(x, y)
        ax.relim()
        ax.autoscale_view()

    plt.pause(0.001)
    newv = samp.val * np.sin(2 * np.pi * sfreq.val * i * Tao)
    set_cir_voltage('V1', newv, cir)
    x = np.concatenate((l2.get_xdata(), [i]))
    y = np.concatenate((l2.get_ydata(), [get_cir_voltage('V1', cir)]))
    l2.set_data(x, y)
    ax1.relim()
    ax1.autoscale_view()

# print cur

# for i in range(len(circ_state[0].results.keys())-1):
#     plt.plot([x.results['VN'+str(i)] for x in circ_state])
# plt.plot([x.results['I(V1)'] for x in circ_state])
#
# plt.show()

# #Get first voltage values
# keys=r.results.keys();
# keys.remove('I(V1)'); #for now we know this key


# create memristors list
# mems={};
# for k in keys:
#     curv=r.results[k];
#     mems[k]=memristor.memristor(w,D,Roff,Ron,mu,Tao,curv);

# connect

# #evolve the system
# for i in range(1000):
# #update circuit resistor values
#     for k in keys:
#         cir.get_elem_by_name(k).
# #calculate circuit
# #update voltages on memristors
# #save values from memristors

# print mems;

# print r
