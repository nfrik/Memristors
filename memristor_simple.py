import matplotlib.pyplot as plt
import numpy as np


class memristor_simple:

    def __init__(self):
        # 900000.0 1500000.0 1.0E-8 1.0E-8 3.0E-18
        self.r_on = 900000;
        self.r_off = 1500000;
        self.dopeWidth = 0;
        self.totalWidth = 10e-9; # meters
        self.mobility = 9*1e-18;   # m^2/sV
        self.resistance = 900000;
        self.volts = 0;
        self.current = 0;

    def calculate_current(self):
        self.current = (self.volts) / self.resistance;

    def do_step(self,timestep):
        self.calculate_current()
        wd = self.dopeWidth / self.totalWidth;
        self.dopeWidth += timestep * self.mobility * self.r_on * self.current / self.totalWidth;
        if self.dopeWidth < 0:
            self.dopeWidth = 0;
        if self.dopeWidth > self.totalWidth:
            self.dopeWidth = self.totalWidth;
        self.resistance = self.r_on * wd + self.r_off * (1 - wd);

    def set_voltage(self,voltage):
        self.volts = voltage;

    def get_current(self):
        return self.current

    def get_resistance(self):
        return self.resistance

    def get_width(self):
        return self.dopeWidth


if __name__ == "__main__":
    f1 = 'SCCNTDRY_terminals_1-2_178.txt'
    f2 = 'SCCNTDRY_terminals_1-2_179.txt'
    d1 = np.genfromtxt('/Users/nfrik/Downloads/parametric files/'+f1,float,delimiter='\t',usecols=(0,1,2,3),skiprows=1)
    d2 = np.genfromtxt('/Users/nfrik/Downloads/parametric files/'+f2,float,delimiter='\t',usecols=(0,1,2,3),skiprows=1)

    mem = memristor_simple()


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
    # plt.plot(t2,icurve)
    plt.plot(vcurve,icurve)
    # plt.plot(d2[:,3],d2[:,0])
    plt.show()

    # icurve=[]
    # wcurve=[]
    # t0=0
    # dt=(d1[10,3]-d1[1,3])/10.0
    # for i in range(len(d1[:,3])):
    #     dt=d1[i,3]-t0
    #     t0=d1[i,3]
    #     mem.set_voltage(voltage=d1[i,0])
    #     mem.do_step(timestep=dt)
    #     icurve.append(mem.get_current())
    #     wcurve.append(mem.get_width())
    #
    # for i in range(len(d2[:,3])):
    #     dt=d2[2,3]-t0
    #     t0=d2[2,3]
    #     mem.set_voltage(voltage=d2[i,0])
    #     mem.do_step(timestep=dt)
    #     icurve.append(mem.get_current())
    #     wcurve.append(mem.get_width())
    #
    # plt.figure()
    # plt.plot(np.append(d1[:,0],d2[:,0]),icurve)
    # # plt.plot(d2[:,3],d2[:,0])
    # plt.figure()
    # plt.plot(np.append(d1[:,3],d2[:,3]),icurve)
    # plt.show()

