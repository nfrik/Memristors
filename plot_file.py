import matplotlib.pyplot as plt
import numpy as np

f1 = 'CNTSDDBS_terminals_A1-B2_278.txt'
f2 = 'CNTSDDBS_terminals_4-5_267.txt'

nplot = 1;

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

plt.figure()
if nplot == 1:
    plt.plot(d1[:,0],d1[:,1],'b-')
else:
    plt.plot(d1[:,0],d1[:,1],'b-',d2[:,0],d2[:,1])
plt.xlabel("V (V)")
plt.ylabel("I (mA)")
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

#combine two data files for V
dv12=np.append(d1[:,0],d2[:,0])
# dv12=d1[:,0]

#min time interval
dt=(d1[10,3]-d1[1,3])/10.0

#get time array
t1=np.array(range(0,len(d1[:,0])))*dt

t2=np.array(range(0,len(dv12)))*dt

fig, ax1 = plt.subplots()
if nplot==1:
    ax1.plot(t1,d1[:,0],'b-')
else:
    ax1.plot(t2,dv12,'b-')
ax1.set_xlabel("Time (sec)")
ax1.set_ylabel("Voltage (V)")

di12=np.append(d1[:,1],d2[:,1])
# di12=d1[:,1]
ax2 = ax1.twinx()
if nplot==1:
    ax2.plot(t1,d1[:,1],'g-')
else:
    ax2.plot(t2,di12,'g-')
ax2.set_ylabel("Current (mA)")


plt.title(f2)

plt.show()