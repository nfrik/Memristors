import numpy as np

# netlist and sources must be numpy objects

class circuit:
    def __init__(self, netlist,sources):
         self.netlist = netlist
         self.sources = sources
         # self.N=max(self.netlist[:,0].ravel().tolist()[0]+self.netlist[:,1].ravel().tolist()[0])
         self.N=max(self.netlist[:,0].tolist()+self.netlist[:,1].tolist())
         self.A = np.zeros((self.N+1,self.N+1))
         self.B = np.zeros((self.N+1,1))

     #setup Kirschoff's equations
    def setupAB(self):
        l=len(self.netlist)
        vn=len(self.sources)

        for i in range(0,l):
            n1=self.netlist[i,0]
            n2=self.netlist[i,1]
            if n1!=n2:
                self.A[n1,n2]=self.A[n1,n2]-1/self.netlist[i,2]
                self.A[n2,n1]=self.A[n2,n1]-1/self.netlist[i,2]
                self.A[n1,n1]=self.A[n1,n1]+1/self.netlist[i,2]
                self.A[n2,n2]=self.A[n2,n2]+1/self.netlist[i,2]

        for i in range(0,vn):
            self.A[self.sources[i,0],:]=np.zeros((1,self.N+1))
            self.A[self.sources[i,0],self.sources[i,0]]=1
            self.B[self.sources[i,0],0]=self.sources[i,1]

    def getV(self): 
        self.setupAB()
        return np.linalg.solve(self.A,self.B)



if __name__ == "__main__":

    netlist = np.array([[0,1,2],[0,2,4],[1,2,5.2],[2,3,6],[1,3,3]])
    sources = np.array([[0,6],[3,2]])
    a=circuit(netlist=netlist,sources=sources)
    v=a.getV()

    print "Voltages: ",v