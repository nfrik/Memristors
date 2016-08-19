from skimage.draw import polygon

from percolation.vectors import *


# v = [3, 4]
# axis = [0, 0, 1]
# theta = 180.*math.pi*2/360.
#
# print theta
# print (dot(rotation_matrix2d(theta), v))

def getRotatedPolygon(L,d,theta,pos):
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
    x = np.array([xy1[0]+pos[0], xy2[0]+pos[0], xy3[0]+pos[0], xy4[0]+pos[1]])
    y = np.array([xy1[1]+pos[1], xy2[1]+pos[1], xy3[1]+pos[1], xy4[1]+pos[1]])

    #produce polygon
    rr, cc = polygon(y, x)
    return rr,cc

xy1=[-5,3]
xy2=[5,3]
xy3=[5,-3]
xy4=[-5,-3]

img1 = zeros((50,50))

x = np.array([xy1[0], xy2[0], xy3[0], xy4[0]])
y = np.array([xy1[1], xy2[1], xy3[1], xy4[1]])
rr, cc = polygon(y, x)

rr,cc = getRotatedPolygon(20,1,45,[20,20])
rr=[r for r in rr]
cc=[c for c in cc]
img1[rr, cc] = 1

figure(figsize=(16,5))
subplot(1,2,1)
imshow(img1,interpolation='nearest')

img2 = zeros((50,50))

theta = 90.*math.pi*2/360.
xy1=dot(rotation_matrix2d(theta), xy1)
xy2=dot(rotation_matrix2d(theta), xy2)
xy3=dot(rotation_matrix2d(theta), xy3)
xy4=dot(rotation_matrix2d(theta), xy4)

x = np.array([xy1[0], xy2[0], xy3[0], xy4[0]])
y = np.array([xy1[1], xy2[1], xy3[1], xy4[1]])
rr, cc = polygon(y, x)
img2[rr, cc] = 1


subplot(1,2,2)
imshow(img2,interpolation='nearest')

show()
