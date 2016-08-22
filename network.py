__author__ = 'nfrik'
import networkx as nx
import matplotlib.pylab as plt
import random
from ahkab import new_ac, new_op, run
from ahkab.circuit import Circuit
import memristor
import numpy as np
from matplotlib.widgets import Slider

graph_type = {1:'watts_strogatz',2:'random_regular'}

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
    plt.figure()
    edge_labels = nx.get_edge_attributes(G, 'weight')
    node_labels = nx.get_node_attributes(G, 'number')

    fig, ax = plt.subplots()
    pos = nx.circular_layout(G)
    # pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, ax=ax)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_size=8, ax=ax)
    nx.draw_networkx_labels(G, pos=pos, labels=node_labels, font_size=8, ax=ax)

    plt.savefig('show2.png')
    plt.close()

def export_graph(G,fname):
    #Currently falstad format only
    # r 272 240 272 160 0 100.0
    file = open(fname,'w')

    #Set XY positions of the nodes
    pos = nx.circular_layout(G,scale=0.25)
    nx.set_node_attributes(G,'pos',pos)

    # $ 0 5.0E-6 1.0312258501325766 50 5.0 50
    file.write('$ %d %1.1E %f %1.2d %1.1f %1.1d\n' % (0,5.0E-6,1.03,50,5.0,50))

    for e in range(0,len(G.edges())):
        x1=G.node[G.edges()[e][0]]['pos'][0]
        y1=G.node[G.edges()[e][0]]['pos'][1]
        x2=G.node[G.edges()[e][1]]['pos'][0]
        y2=G.node[G.edges()[e][1]]['pos'][1]
        # file.write('r %d %d %d %d %d %1.1f\n' % (x1*1000,y1*1000,x2*1000,y2*1000,0,50.0))
        # m 432 192 432 304 0 100.0 16000.0 0.0 1.0E-8 1.0E-10
        file.write('m %d %d %d %d %d %1.1f %1.1f %1.1f %1.1E %1.1E\n' % (x1*1000,y1*1000,x2*1000,y2*1000,0,100.0,16000.0,0.0,1.0E-8,1.0E-10));

    file.close()

def generate_network(mem_pars, net_pars):
    if net_pars['type']==graph_type[1]:
        G = nx.watts_strogatz_graph(net_pars['N'],net_pars['k'],net_pars['p'])
    elif net_pars['type']==graph_type[2]:
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

    # Add random ground and voltage terminal nodes
    [v1, gnd] = random.sample(xrange(0, len(G.nodes())), 2)
    lastnode = len(G.nodes())
    G.add_edge(v1, lastnode)
    G.node[lastnode]['number'] = 'V1'
    lastnode += 1
    G.add_edge(gnd, lastnode)
    G.node[lastnode]['number'] = 'gnd'

    plot_graph(G)

    export_graph(G,'/Users/nfrik/CloudStation/Research/LaBean/ESN/FalstadSPICE/test.txt')

    cir.add_resistor("RG", 'n' + str(gnd), cir.gnd, 0.001)
    cir.add_vsource("V1", 'n' + str(v1), cir.gnd, 1000)
    opa = new_op()

    # netdict contains setup graph and circuit
    networkdict = {}
    networkdict['Graph'] = G
    networkdict['Circuit'] = cir
    networkdict['Memristors'] = memdict
    networkdict['Opa']=opa

    return networkdict


w = 0.1
D = 1.0
Roff = 100.
Ron = 1.
mu = 10.
Tao = 0.1

mem_pars = {'w': w, 'D': D, 'Roff': Roff, 'Ron': Ron, 'mu': mu, 'Tao': Tao}

net_pars = {'degree': 3, 'N': 30, 'type':graph_type[1],'k':3,'p':0.2}

netdict = generate_network(mem_pars, net_pars)

global a0, f0
a0 = 1000
f0 = 10


circ_state = []
x = 0
y = 0
fig = plt.figure(1)
ax = fig.add_subplot(211)
ax1 = fig.add_subplot(212)
plt.subplots_adjust(left=0.25, bottom=0.25)

r = run(netdict['Circuit'], netdict['Opa'])['op']
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
    r = run(netdict['Circuit'], netdict['Opa'])['op']
    netdict=update_memristor_vals_from_oprun(netdict,r)
    netdict=update_memristor_states(netdict)
    netdict=update_circrvals_from_memres(netdict)
    circ_state.append(r)

    for p in range(len(r.results.keys()) - 1):
        x = np.concatenate((line[p].get_xdata(), [i]))
        y = np.concatenate((line[p].get_ydata(), [r.results['VN' + str(p)]]))
        line[p].set_data(x, y)
        ax.relim()
        ax.autoscale_view()

    plt.pause(0.001)
    newv = samp.val * np.sin(2 * np.pi * sfreq.val * i * Tao)
    set_cir_voltage('V1', newv, netdict)
    x = np.concatenate((l2.get_xdata(), [i]))
    y = np.concatenate((l2.get_ydata(), [get_cir_voltage('V1', netdict)]))
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
