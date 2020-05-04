# import matplotlib.pyplot as plt
# import numpy as np
# from mpl_toolkits.mplot3d import Axes3D
# from scipy import interpolate
#
#
# x = np.arange(-5.01, 5.01, 0.25)
#
# y = np.arange(-5.01, 5.01, 0.25)
# xx, yy = np.meshgrid(x, y)
# z = np.sin(xx**2+yy**2)
# plt.mesh(X,Y,Z)
# # f = interpolate.interp2d(x, y, z, kind='cubic')
# # xnew = np.arange(-5.01, 5.01, 1e-2)
# # ynew = np.arange(-5.01, 5.01, 1e-2)
# # znew = f(xnew, ynew)
# # #plt.plot(x, z[0, :], 'ro', xnew, znew[0, :], 'b')
# # plt.plot3(x,y,z)
# # plt.show()


from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
# fig = plt.figure()
# ax = Axes3D(fig)
# X = np.arange(-4, 4, 2)
# Y = np.arange(-4, 4, 2)
# X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
# Z = np.sin(R)
# f = interpolate.interp2d(X, Y, Z, kind='cubic')
# X1 = np.arange(-4, 4, 0.25)
# Y1 = np.arange(-4, 4, 0.25)
#
# Z1 = f(X1, Y1)
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
# #ax.plot_surface(X1, Y1, Z1, rstride=1, cstride=1, cmap='rainbow')
# #ax.contourf(X, Y, Z, zdir='z', offset=0, cmap=plt.get_cmap('rainbow'))#projection
#
# plt.show()


x = np.arange(-5.01, 5.01, 0.25)
y = np.arange(-5.01, 5.01, 0.25)
xx, yy = np.meshgrid(x, y)
z = np.sin(xx**2+yy**2)
f = interpolate.interp2d(x, y, z, kind='linear')

xnew = np.arange(-5.01, 5.01, 1e-2)
ynew = np.arange(-5.01, 5.01, 1e-2)
znew = f(xnew, ynew)
