import matplotlib.pyplot as plt
import numpy as np
import memristor_simple

f1 = 'SCCNTDRY_terminals_1-2_178.txt'
f2 = 'SCCNTDRY_terminals_1-2_179.txt'

nplot = 2;

model_only = False;

d1 = np.genfromtxt('/Users/nfrik/Downloads/parametric files/'+f1,float,delimiter='\t',usecols=(0,1,2,3),skiprows=1)
d2 = np.genfromtxt('/Users/nfrik/Downloads/parametric files/'+f2,float,delimiter='\t',usecols=(0,1,2,3),skiprows=1)
# d3 = np.genfromtxt('/Users/nfrik/Downloads/parametric files/TOT_triangle_37.txt',float,delimiter='\t',usecols=(0,1,2,3),skiprows=1)
# d4 = np.genfromtxt('/Users/nfrik/Downloads/parametric files/TOT_triangle_38.txt',float,delimiter='\t',usecols=(0,1,2,3),skiprows=1)
# d5 = np.genfromtxt('/Users/nfrik/Downloads/parametric files/TOT_triangle_39.txt',float,delimiter='\t',usecols=(0,1,2,3),skiprows=1)
# d6 = np.genfromtxt('/Users/nfrik/Downloads/parametric files/TOT_triangle_40.txt',float,delimiter='\t',usecols=(0,1,2,3),skiprows=1)

# data = [row for row in data if row[1]<1e8]

# d1 = d1[data1[:,1]<1e8]

# data2 = data2[data2[:,1]<1e8]
# data3 = data3[data3[:,1]<1e8]
# data4 = data4[data4[:,1]<1e8]

# x,y = [data[i,0],data[i,1] for i in ]


mem = memristor_simple.memristor_simple()

#combine two data files for V
dv12=np.append(d1[:,0],d2[:,0])
dt12=np.append(d1[:,3],d2[:,3])
# dv12=d1[:,0]

#min time interval
dt=(d1[100,3]-d1[1,3])/100.0

#get time array
t1=np.array(range(0,len(d1[:,0])))*dt

t2=np.array(range(0,len(dv12)))*dt

icurve=[]
wcurve=[]
tcurve=[]
vcurve=[]
t_old=0;

for i in range(len(d1[:,3])):
    # dt=d1[i,3]-t_old
    # t_old+=dt
    mem.set_voltage(voltage=d1[i,0])
    mem.do_step(timestep=dt)
    icurve.append(mem.get_current()*1e6)
    wcurve.append(mem.get_width())
    vcurve.append(d1[i,0])
    # tcurve.append(t_old)

t0=0
for i in range(len(d2[:,3])):
    # dt=d2[i,3]-t0
    # t0=d2[i,3]
    # t_old+=dt
    mem.set_voltage(voltage=d2[i,0])
    mem.do_step(timestep=dt)
    icurve.append(mem.get_current()*1e6)
    wcurve.append(mem.get_width())
    vcurve.append(d2[i,0])
    # tcurve.append(t_old)


plt.figure()
if not model_only:
    if nplot == 1:
        plt.plot(d1[:,0],[z*1000 for z in d1[:,1]],'k-',linewidth=1)
    else:
        plt.plot(d1[:,0],[z*1000 for z in d1[:,1]],'k-',d2[:,0],[z*1000 for z in d2[:,1]],'k-',linewidth=1)
else:
        plt.plot(vcurve,icurve,'k-',linewidth=1)

plt.xlabel("Voltage (V)")
plt.ylabel("Current (uA)")
plt.title(f1)
# #
# plt.plot(d4[:,0],d4[:,1],'b-',d5[:,0],d5[:,1],'r-',d6[:,0],d6[:,1],'g-')

# plt.plot(data1[:,0],data1[:,1],'b-')

# plt.plot(p1[:,0],p1[:,1],'b-',p2[:,0],p2[:,1],'r-',p3[:,0],p3[:,1],'g-')

# plt.plot(d1[:,0],d1[:,1],'g-')
# plt.xlabel("V (V)")
# plt.ylabel("I (mA)")
#
#
# d1=d1[d1[:,0]>0]

#
#

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)




# t1=d1[:,3]
# t1=np.array(t1)
#
# t2=np.append(np.array(d1[:,3]),np.array(d2[:,3])+d1[-1,3])



fig, ax1 = plt.subplots(2, sharex=True)
# plt.title(f2)
ax1[0].set_title(f2)

if nplot==1:
    ax1[0].plot(t1,d1[:,0],'g-',linewidth=2)
else:
    ax1[0].plot(t2,dv12,'g-',linewidth=2)
ax1[1].set_xlabel("Time (sec)")
ax1[0].set_ylabel("Voltage (V)")
# for tl in ax1[0].get_yticklabels():
#     tl.set_color('g');


di12=np.append(d1[:,1],d2[:,1])
# di12=d1[:,1]

# ax2 = ax1.twinx()
if nplot==1:
    ax1[1].plot(t1,[z*1000 for z in d1[:,1]],'b-',linewidth=2)
else:
    ax1[1].plot(t2,[z*1000 for z in di12],'b-',linewidth=2)
    # ax2.plot(t2,icurve,'r-')

ax1[1].set_ylabel("Current (uA)")
# for tl in ax1[1].get_yticklabels():
#     tl.set_color('b');


# align_yaxis(ax1,0,ax2,-5)



plt.show()