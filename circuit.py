import numpy as np

class circuit:
    def __init__(self, netlist,sources):
         self.netlist = netlist
         self.sources = sources
         self.A = np.zeros(0)
         self.B = np.zeros(0)

     #setup Kirschoff's equations
    def setupEQ(self):
        return 0;

    def getV(self):
        return 0;


if __name__ == "__main__":
    print "hello!"