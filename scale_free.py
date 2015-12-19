import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import igraph as ig
from matplotlib.widgets import Slider


def func(x,a,b,c):
    return a*np.exp(-b*x)+c

def powf(x,a,b,c):
    return a*np.power(x,-b)+c

def getPowerGraphs(n,p):
    g=ig.Graph.Barabasi(n,power=p)
    G=nx.Graph(g.get_edgelist())
    return [g,G]

def calc_fit(G):
    degree_sequence = sorted(nx.degree(G).values(), reverse=True)
    degree_sequence = [float(i) / sum(degree_sequence) for i in degree_sequence]
    xdata = range(1, len(degree_sequence) + 1)
    popt, pcov = curve_fit(powf, xdata, degree_sequence)
    return [xdata,degree_sequence,popt, pcov]


fig, (ax1,ax2) = plt.subplots(2,1)
plt.subplots_adjust(left=0.25,bottom=0.25)
n0=100
p0=1.2

[g,G]=getPowerGraphs(n0,p0)


pos = nx.spring_layout(G,iterations=20)
nx.draw(G, pos,ax=ax1,node_size=50)

[xdata,degree_sequence,popt,pcov] = calc_fit(G)
ax2.plot(degree_sequence)
ax2.plot(powf(xdata,popt[0],popt[1],popt[2]))
ax2.set_title("gamma="+str(round(popt[1],1)))

axcolor = 'lightgoldenrodyellow'
axnump = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
apower = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

snump = Slider(axnump, 'Number', 10., 1000.0, valinit=n0)
spower = Slider(apower, 'Power', 0.1, 5.0, valinit=p0)


def update(val):
    n=int(snump.val)
    p=spower.val
    [g,G]=getPowerGraphs(n,p)
    pos = nx.spring_layout(G,iterations=20)
    ax1.clear()
    ax2.clear()
    nx.draw(G, pos,ax=ax1,node_size=50)

    [xdata,degree_sequence,popt,pcov] = calc_fit(G)
    ax2.plot(degree_sequence)
    ax2.plot(powf(xdata,popt[0],popt[1],popt[2]))
    ax2.set_title("gamma="+str(round(popt[1],1)))


    plt.show()
    fig.canvas.draw_idle()

snump.on_changed(update)
spower.on_changed(update)

plt.show()


#
#
#
# layout = g.layout("rt")
# ig.plot(g)
#
# degree_sequence=sorted(nx.degree(G).values(),reverse=True)
# degree_sequence = [float(i)/sum(degree_sequence) for i in degree_sequence]
#
# xdata = range(1,len(degree_sequence)+1)
# # y = powf(xdata,10.,3.,.1)#+0.02*np.random.normal(size=len(xdata))
#
#
#
#
#
# plt.figure()
# pos = nx.spring_layout(G)
# nx.draw(G, pos)
# plt.show()
#
# plt.figure()
# popt, pcov = curve_fit(powf,xdata,degree_sequence)
# plt.plot(degree_sequence)
# plt.plot(powf(xdata,popt[0],popt[1],popt[2]))
# # plt.loglog(degree_sequence,'b-',marker='o')
# # plt.loglog(powf(xdata,popt[0],popt[1],popt[2]))
# plt.show()
#
# #
# print popt
# print pcov
