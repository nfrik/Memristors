from pylab import *
from skimage.draw import polygon, circle
import math

def rotation_matrix3d(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = asarray(axis)
    theta = asarray(theta)
    axis = axis/math.sqrt(dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])

def rotation_matrix2d(theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    return array([[math.cos(theta), -math.sin(theta)],
                     [math.sin(theta), math.cos(theta)]])

def getRotatedPolygon(L,d,theta,shape=[],posx=0,posy=0):
    xy1=[-L/2,d/2]
    xy2=[L/2,d/2]
    xy3=[L/2,-d/2]
    xy4=[-L/2,-d/2]

    theta = theta*2.*math.pi/360

    #rotate each coordinate as a vector
    xy1=dot(rotation_matrix2d(theta), xy1)
    xy2=dot(rotation_matrix2d(theta), xy2)
    xy3=dot(rotation_matrix2d(theta), xy3)
    xy4=dot(rotation_matrix2d(theta), xy4)

    #construct input arrays
    x = np.array([xy1[0]+posx, xy2[0]+posx, xy3[0]+posx, xy4[0]+posx])
    y = np.array([xy1[1]+posy, xy2[1]+posy, xy3[1]+posy, xy4[1]+posy])


    #produce polygon
    rr, cc = polygon(y, x, shape)
    return rr,cc


def getCircle(r,shape=[],posx=0,posy=0):
    rr,cc = circle(posx,posy,r,shape)
    return rr, cc