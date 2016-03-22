import csv
import numpy
import DC_plotting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

reader=csv.reader(open("./dc_quads_coarse.csv","rb"),delimiter=';')
x=list(reader)
quads=numpy.array(x).astype('int')

reader=csv.reader(open("./dc_verts_coarse.csv","rb"),delimiter=';')
x=list(reader)
verts=numpy.array(x).astype('float')

reader=csv.reader(open("./dc_non_manifold_edges.csv","rb"),delimiter=';')
x=list(reader)
non_manifolds = numpy.array(x).astype('int')

reader=csv.reader(open("./dc_dimensions.csv","rb"),delimiter=';')
x=list(reader)
dims_raw = numpy.array(x).astype('float')

print quads

dimensions = {}
dimensions['xmin']=dims_raw[0,0]
dimensions['ymin']=dims_raw[0,1]
dimensions['zmin']=dims_raw[0,2]

dimensions['xmax']=dims_raw[1,0]
dimensions['ymax']=dims_raw[1,1]
dimensions['zmax']=dims_raw[1,2]

fig = plt.figure()
ax = Axes3D(fig)

DC_plotting.plot_surface(axis=ax, quads=quads, verts=verts, color='b', alpha=.5)
DC_plotting.plot_edge(axis=ax, edges=non_manifolds, verts=verts, color='r', linewidth=5)

x_mean = (dimensions['xmax']-dimensions['xmin'])/2.0
y_mean = (dimensions['ymax']-dimensions['ymin'])/2.0
z_mean = (dimensions['zmax']-dimensions['zmin'])/2.0

x_min = dimensions['xmin']
y_min = dimensions['ymin']
z_min = dimensions['zmin']
minmin = min([x_min, y_min, z_min])

x_max = dimensions['xmax']
y_max = dimensions['ymax']
z_max = dimensions['zmax']
maxmax = max([x_max, y_max, z_max])

width = maxmax-minmin

ax.set_xlim3d(x_mean-width*.5, x_mean+width*.5)
ax.set_ylim3d(y_mean-width*.5, y_mean+width*.5)
ax.set_zlim3d(z_mean-width*.5, z_mean+width*.5)
ax.set_aspect('equal')

plt.show()
