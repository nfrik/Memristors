from vectors import *
from percolationclusters import *
from pylab import *

if __name__=="__main__":

    #Dimensions of the system
    Lx=400
    Ly=400

    #Define rods
    Nr=60   #rods
    Lr=100 #lenght of rod in nm
    Dr=3  #diameter of rod in nm

    #Define circles
    Nc=0   #rods
    Rc=20 #lenght of rod in nm

    #Define 1x1 nm particles
    Np=10000 #particles
    p=float(Np)/(Lx*Ly)

    #Create random matrix
    # r = rand(Lx+Lr+1,Ly+Lr+1)
    # r=zeros((Lx+Lr+1,Ly+Lr+1))
    # r = r < p

    ncount = 0
    perc = []

    while (len(perc)==0):
        ncount = ncount + 1
        if (ncount >100):
            #print "Couldn't make percolation cluster..."
            break

        #Generate experimental playground
        z=rand(Lx,Ly)<p

        if Nr>0:
            #Locations of rods
            rx=random_integers(0,Lx,Nr)
            ry=random_integers(0,Ly,Nr)

            for i in range(len(rx)):
                pos=[rx[i],ry[i]]
                rr, cc = getRotatedPolygon(Lr,Dr,random()*360,[Lx,Ly],rx[i],ry[i])
                z[rr,cc]=1


        if Nc>0:
            #Locations of circles
            rx=random_integers(0,Lx,Nc)
            ry=random_integers(0,Ly,Nc)

            for i in range(len(rx)):
                pos=[rx[i],ry[i]]
                rr, cc = getCircle(Rc,[Lx,Ly],rx[i],ry[i])
                z[rr,cc]=1

        lw,num = measurements.label(z)
        perc_x = intersect1d(lw[0,:],lw[-1,:])
        perc = perc_x[where(perc_x > 0)]
        print "Percolation attempt", ncount


    #print "z="
    #print z*1
#    labelList = arange(num + 1)
#    clusterareas = measurements.sum(z, lw, index=labelList)
#    areaImg = clusterareas[lw]
#    maxarea = clusterareas.max()
    zz = asarray((lw == perc[0]))
    # zz now contains the spanning cluster
    # Transpose
    zzz = zz.T
#    # Generate bond lattice from this
    g = sitetobond ( zzz )
#    figure()
#    imshow(g[:,0].reshape(Lx,Ly), interpolation='nearest')
#    figure()
#    imshow(g[:,1].reshape(Lx,Ly), interpolation='nearest')
#    figure()
#    imshow(zzz, interpolation='nearest')
#    # Generate conductivity matrix
    p, c_eff = FIND_COND (g, Lx, Ly)
#    # Transform this onto a nx x ny lattice
    x = coltomat ( p , Lx , Ly )
    P = x * zzz
    g1 = g[:,0]
    g2 = g[: ,1]
    z1 = coltomat( g1 , Lx , Ly )
    z2 = coltomat( g2 , Lx , Ly )
#    # Plotting
    fig=figure()
    ax = subplot(221)
    zm=asarray(z)
    imshow(zm.T, interpolation='nearest')
    title("Initial System of Particles")
    grid(color="white")
#    subplot (2 ,2 ,1) , imagesc ( zzz )
#    title ( " Spanning cluster ")
#    axis equal
    subplot(222, sharex=ax, sharey=ax)
    imshow(P, interpolation='nearest')
    title("Electric Potential for spanning cluster")
    colorbar()
    grid(color="white")
#    subplot (2 ,2 ,2) , imagesc ( P )
#    title ( " Pressure " )
#    axis equal

    # Calculate flux from top to down (remember that flux is the negative of the pressure difference)
    f2 = zeros ( (Lx , Ly ))
    for iy in range(Ly -1):
        f2[: , iy ] = ( P [: , iy ] - P [: , iy +1]) * z2 [: , iy ]

    # Calculate flux from left to right (remember that flux is the negative of the pressure difference)
    f1 = zeros ( (Lx , Ly ))
    for ix in range(Lx-1):
        f1[ ix ,:] = ( P [ ix ,:] - P [ ix +1 ,:]) * z1 [ ix ,:]
#
#    # Find the sum of absolute fluxes in and out of each site
    fn = zeros (( Lx , Ly ))
    fn = fn + abs ( f1 )
    fn = fn + abs ( f2 )
    # Add for each column, except the leftmost one, the up-down flux, but offset
    fn [: ,1: Ly ] = fn [: ,1: Ly ] + abs ( f2 [: ,0: Ly -1])
    # For the left-most one, add the inverse pressure multiplied with the spanning cluster bool information
    fn [: ,0] = fn [: ,0] + abs (( P [: ,0] - 1.0)*( zzz [: ,0]))
    # For each row except the topmost one, add the left-right flux, but offset
    fn [1: Lx ,:] = fn [1: Lx ,:] + abs ( f1 [0: Lx -1 ,:])
    subplot(223, sharex=ax, sharey=ax)
    imshow(fn, interpolation='nearest')
    title ( " Electron Flux " )
    colorbar()
    grid(color="white")

    #print "fn"
    #print fn
#    subplot (2 ,2 ,3) , imagesc ( fn )
    zfn = fn > fn.max() - 1e-6
    zbb = ( zzz + 2* zfn )
    zbb = zbb / zbb.max()
    subplot(224, sharex=ax, sharey=ax)
    imshow(zbb, interpolation='nearest')
#    subplot (2 ,2 ,4) , imagesc ( zbb )
    title ( " BB and DE ")
    grid(color="white")


    text(0.5, 0.95, 'System composition: Rods: '+str(Nr)+', Circles: '+str(Nc)+', 1x1 nm particles: '+str(Np), transform=fig.transFigure, horizontalalignment='center')

    show()











    # # figure(figsize=(16,5))
    # figure()
    # subplot(1,2,2)
    # lw, num = measurements.label(z)
    # b = arange(lw.max() + 1) # create an array of values from 0 to lw.max() + 1
    # shuffle(b) # shuffle this array
    # shuffledLw = b[lw] # replace all values with values from b
    # imshow(shuffledLw,interpolation='nearest')
    # colorbar()
    # title("Cluster matrix")
    # show()


    # figure(figsize=(16,5))
    #
    # subplot(1,2,1)
    # imshow(r,interpolation='nearest')
    # title("Actual distribution")
    # colorbar()
    #
    # subplot(1,2,2)
    # lw, num = measurements.label(r)
    # b = arange(lw.max() + 1) # create an array of values from 0 to lw.max() + 1
    # shuffle(b) # shuffle this array
    # shuffledLw = b[lw] # replace all values with values from b
    # imshow(shuffledLw,interpolation='nearest')
    # colorbar()
    # title("Cluster matrix")
    #
    # show()