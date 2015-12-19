__author__ = 'nfrik'
import time
import matplotlib.pyplot as plt
import math
import numpy as np

class memristor:
    # def __init__(self, w, D, Roff, Ron, v, mu, Tao):
    def __init__(self, w, D, Roff, Ron, mu, Tao,v):
        self.w = w #Width of the TiO(2-X) layer
        self.Roff = Roff #Resistance Off value
        self.Ron  = Ron #Resistance On value
        self.v    = v #Voltage
        self.D    = D #Width of the TiO layer
        self.mu   = mu #Mobility
        self.Tao  = Tao #Time parameter
        self.RonMRoffD=(self.Ron-self.Roff)/self.D
        self.RoffSq=np.power(self.Roff,2)
        self.muRonDdt=self.mu*self.Ron/self.D*self.Tao

    def setV(self,v):
        self.v = v

    def getV(self):
        return self.v

    def updateW(self):

        estim = self.getNewW()
        if estim<self.D and estim > 0.0:
            self.w=self.getNewW()

    def getNewW(self):
        # if self.exact <> True:
            return self.w+self.Ron/self.D*self.v/(self.Ron*self.w/self.D+self.Roff*(1-self.w/self.D))*self.Tao/1.0
        # else:
        #     return (-self.Roff+np.sqrt(self.RoffSq+2*self.RonMRoffD*(self.RonMRoffD/2*np.power(self.w,2)+self.Roff*self.w+self.muRonDdt*self.v)))/self.RonMRoffD

    # def getNewExW(self):
    #     # return (np.sqrt(np.power(self.Roff,2)+(self.Ron-self.Roff)/self.D*((self.Ron-self.Roff)*np.power(self.w,2)/2/self.D+self.Roff*self.w+self.mu*self.Ron/self.D*self.v*self.Tao))-self.Roff)/(self.Ron-self.Roff)/self.D
    #     return (-self.Roff+np.sqrt(self.RoffSq+2*self.RonMRoffD*(self.RonMRoffD/2*np.power(self.w,2)+self.Roff*self.w+self.muRonDdt*self.v)))/self.RonMRoffD

    def getW(self):
        return self.w

    def getR(self):
        return (self.Ron*self.w/self.D+self.Roff*(1-self.w/self.D))

    def getI(self):
        return self.getV()/self.getR()


if __name__ == "__main__":

    # Define a function for the thread
    def print_time( threadName, delay):
       count = 0
       while count < 5:
          time.sleep(delay)
          count += 1
          print "%s: %s" % ( threadName, time.ctime(time.time()) )


    mem1 = memristor(0.1,1.0,10000.0,10.0,10.0,0.01,10.0)


    yw=[]
    yr=[]
    yi=[]
    xv=[]

    for i in range(10000):
        yw.append(mem1.getW())
        yi.append(mem1.getI())
        yr.append(mem1.getR())
        xv.append(mem1.getV())
        mem1.updateW()
        mem1.setV(10*math.sin(2*math.pi*i/10000))
        # print "W= "+str(mem1.getW()) + " R= " + str(mem1.getR()) + " V= " + str(mem1.getV()) + " I= " + str(mem1.getI());

    # plt.figure(1)
    # plt.plot(xv,yi);
    plt.figure(1)
    plt.subplot(411)
    plt.plot(range(len(xv)),xv,'b-')
    plt.title("Voltage")
    plt.subplot(412)
    plt.plot(range(len(xv)),yi,'g-')
    plt.title("Current")
    plt.subplot(413)
    plt.plot(range(len(xv)),yr,'rs')
    plt.title("Resistance")
    plt.subplot(414)
    plt.plot(range(len(xv)),yw)
    plt.title("W")


    plt.figure(2)
    plt.plot(xv[1::],yi[1::],'r-')
    plt.show()


    print str(min(yr))
    # # Create two threads as follows
    # try:
    #    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    #    thread.start_new_thread( print_time, ("Thread-2", 4, ) )
    # except:
    #    print "Error: unable to start thread"
    #
    # while 1:
    #    pass





# __author__ = 'nfrik'
# import thread
# import time
# import matplotlib.pyplot as plt;
# import math;
#
# class memristor:
#     # def __init__(self, w, D, Roff, Ron, v, mu, Tao):
#     def __init__(self, w, D, Roff, Ron, mu, Tao,v):
#         self.w = w; #Width of the TiO(2-X) layer
#         self.Roff = Roff; #Resistance Off value
#         self.Ron  = Ron; #Resistance On value
#         self.v    = v; #Voltage
#         self.D    = D; #Width of the TiO layer
#         self.mu   = mu; #Mobility
#         self.Tao  = Tao; #Time parameter
#
#     def setV(self,v):
#         self.v = v;
#
#     def getV(self):
#         return self.v;
#
#     def updateW(self):
#
#         estim = self.getNewW();
#         if estim<self.D and estim > 0.0:
#             self.w=self.getNewW();
#
#     def getNewW(self):
#         return self.w+self.Ron/self.D*self.v/(self.Ron*self.w/self.D+self.Roff*(1-self.w/self.D))*self.Tao/1000.0;
#
#     def getW(self):
#         return self.w
#
#     def getR(self):
#         return (self.Ron*self.w/self.D+self.Roff*(1-self.w/self.D));
#
#     def getI(self):
#         return self.getV()/self.getR();
#
#
# if __name__ == "__main__":
#
#     # Define a function for the thread
#     def print_time( threadName, delay):
#        count = 0
#        while count < 5:
#           time.sleep(delay)
#           count += 1
#           print "%s: %s" % ( threadName, time.ctime(time.time()) )
#
#
#     mem1 = memristor(0.1,1.0,10000.0,10.0,10.0,0.01,10.0);
#
#
#     yw=[];
#     yr=[];
#     yi=[];
#     xv=[];
#
#     for i in range(10000):
#         yw.append(mem1.getW())
#         yi.append(mem1.getI())
#         yr.append(mem1.getR())
#         xv.append(mem1.getV())
#         mem1.updateW();
#         mem1.setV(10*math.sin(2*math.pi*i/10000))
#         # print "W= "+str(mem1.getW()) + " R= " + str(mem1.getR()) + " V= " + str(mem1.getV()) + " I= " + str(mem1.getI());
#
#     # plt.figure(1)
#     # plt.plot(xv,yi);
#     plt.figure(1)
#     plt.subplot(411)
#     plt.plot(range(len(xv)),xv,'b-');
#     plt.subplot(412)
#     plt.plot(range(len(xv)),yi,'g-');
#     plt.subplot(413)
#     plt.plot(range(len(xv)),yr,'rs')
#     plt.subplot(414)
#     plt.plot(range(len(xv)),yw)
#
#     plt.figure(2)
#     plt.plot(xv,yi,'r.')
#     plt.show()
#
#
#     print str(min(yr))
#     # # Create two threads as follows
#     # try:
#     #    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#     #    thread.start_new_thread( print_time, ("Thread-2", 4, ) )
#     # except:
#     #    print "Error: unable to start thread"
#     #
#     # while 1:
#     #    pass
