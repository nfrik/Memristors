from skimage.draw import polygon

from vectors import getRotatedPolygon
from scipy.ndimage import measurements
from pylab import *
from scipy.sparse import spdiags, dia_matrix, coo_matrix
from scipy.sparse.linalg import spsolve
from numpy.linalg import solve

#
# Written by Marin Soreng
# ( C ) 2004
#
# Calculates the effective flow conductance Ceff of the
# lattice A as well as the pressure P in every site .
def FIND_COND (A , X , Y ):
    P_in = 1.
    P_out = 0.
    # Calls MK_EQSYSTEM .
    B,C = MK_EQSYSTEM (A , X , Y )
    #print "B"
    #print B.todense()
    #print "C"
    #print C
    # Kirchhoff equations solve for P
    P = spsolve(B, C)
    # print len(B.toarray())
    # print len(C)
    # P=solve(B.toarray(),C)

    # The pressure at the external sites is added
    # ( Boundary conditions )
    P = concatenate((P_in * ones (X), P,  P_out * ones (X)))
    # Calculate Ceff
    Ceff = (P[-1-2*X+1:-1-X] - P_out).T * A[-1-2*X+1:-1-X, 1] / ( P_in - P_out )
    #print "P"
    #print P
    #print "Ceff"
    #print Ceff
    return P , Ceff

#
# Written by Marin S r e n g
# ( C ) 2004
#
# Sets up Kirchoff's equations for the 2 D lattice A .
# A has X * Y rows and 2 columns . The rows indicate the site ,
# the first column the bond perpendicular to the flow direction
# and the second column the bond parallel to the flow direction .
#
# The return values are [B , C ] where B * x = C . This is solved
# for the site pressure by x = B \ C .

def MK_EQSYSTEM (A , X , Y ):
    # Total no of internal lattice sites
    sites = X *( Y - 2)
    #print "sites:", sites
    # Allocate space for the nonzero upper diagonals
    main_diag = zeros(sites)
    upper_diag1 = zeros(sites - 1)
    upper_diag2 = zeros(sites - X)
    # Calculates the nonzero upper diagonals
    #print A
    upper_diag1 = A[X:X*(Y-1)-1, 0]
    upper_diag2 = A[X:X*(Y-2), 1]
    main_diag = A[X:X*(Y-1), 0] + A[X:X*(Y-1), 1] + A[0:X*(Y-2), 1] + A[X-1:X*(Y-1)-1, 0]
    main_diag[where(main_diag == 0)] = 1
    # B = dia_matrix ((sites , sites))
    # Constructing B which is symmetric , lower = upper diagonals .
    # B *u = t
    B = - spdiags ( upper_diag1 , -1 , sites , sites )
    B = B + - spdiags ( upper_diag2 ,-X , sites , sites )
    B = B + B.T + spdiags ( main_diag , 0 , sites , sites )
    # Constructing C
    C = zeros(sites)
    #    C = dia_matrix ( (sites , 1) )
    C[0:X] = A[0:X, 1]
    C[-1-X+1:-1] = 0*A [-1 -2*X + 1:-1-X, 1]
    return B , C

def sitetobond ( z ):
    #
    # Function to convert the site network z (L , L ) into a ( L *L ,2) bond
    # network
    # g [i,0] gives bond perpendicular to direction of flow
    # g [i,1] gives bond parallel to direction of flow
    # z [ nx , ny ] -> g [ nx * ny , 2]
    #
    nx = size (z ,1 - 1)
    ny = size (z ,2 - 1)
    N = nx * ny
    # g = zeros (N ,2)
    gg_r = zeros ((nx , ny)) # First , find these
    gg_d = zeros ((nx , ny )) # First , find these
    gg_r [:, 0:ny - 1] = z [:, 0:ny - 1] * z [:, 1:ny]
    gg_r [: , ny  - 1] = z [: , ny  - 1]
    gg_d [0:nx - 1, :] = z [0:nx - 1, :] * z [1:nx, :]
    gg_d [nx - 1, :] = 0
    #print "gg_r"
    #print gg_r
    #print "gg_d"
    #print gg_d
    # Then , concatenate gg onto g
    g = zeros ((nx *ny ,2))
    g [:, 0] = gg_d.reshape(-1,order='F').T
    g [:, 1] = gg_r.reshape(-1,order='F').T
    return g

def coltomat (z, x, y):
    # Convert z ( x * y ) into a matrix of z (x , y )
    # Transform this onto a nx x ny lattice
    g = zeros ((x , y))
    #print "For"
    for iy in range(1,y):
        i = (iy - 1) * x + 1
        ii = i + x - 1
        #print iy, i, ii
        g[: , iy - 1] = z[ i - 1 : ii]
    return g

if __name__=="__main__":

    #Dimensions of the system
    Lx=1000
    Ly=1000

    #Number of particles
    Nr=500   #rods
    Lr=100 #lenght of rod in nm
    Dr=4  #diameter of rod in nm

    Np=100 #particles
    p=float(Np)/(Lx*Ly)

    #Create random matrix
    r = rand(Lx+Lr+1,Ly+Lr+1)
    # r=zeros((Lx+Lr+1,Ly+Lr+1))
    r = r < p

    #Locations of rods
    rx=random_integers(Lr/2,Lx+Lr/2,Nr)
    ry=random_integers(Lr/2,Ly+Lr/2,Nr)

    for i in range(len(rx)):
        pos=[rx[i],ry[i]]
        rr, cc = getRotatedPolygon(Lr,Dr,random()*360,rx[i],ry[i])
        r[rr,cc]=1


    figure(figsize=(16,5))

    subplot(1,2,1)
    imshow(r,interpolation='nearest')
    title("Actual distribution")
    colorbar()

    subplot(1,2,2)
    lw, num = measurements.label(r)
    b = arange(lw.max() + 1) # create an array of values from 0 to lw.max() + 1
    shuffle(b) # shuffle this array
    shuffledLw = b[lw] # replace all values with values from b
    imshow(shuffledLw,interpolation='nearest')
    colorbar()
    title("Cluster matrix")

    show()