from __future__ import division
import numpy as np

__author__ = 'benjamin'


def sample_data(f, res, dims):
    if (dims.__len__() / 2) == 2:
        return sample_data2D(f, res, dims)
    elif (dims.__len__() / 2) == 3:
        return sample_data3D(f, res, dims)
    else:
        print "ERROR!"
        quit()


def sample_data3D(f, res, dims):

    import itertools as it

    data = {}
    for x, y, z in it.product(np.arange(dims['xmin'], dims['xmax']+res, res), np.arange(dims['ymin'], dims['ymax']+res, res), np.arange(dims['zmin'], dims['zmax']+res, res)):
        key = (x, y, z)
        x_vec = np.array([x, y, z])
        data[key] = f(x_vec)
    return data


def sample_data2D(f, res, dims):
    import numpy as np
    import itertools as it

    data = {}
    for x, y in it.product(np.arange(dims['xmin'], dims['xmax']+res, res), np.arange(dims['ymin'], dims['ymax']+res, res)):
        key = (x, y)
        x_vec = np.array([x, y])
        data[key] = f(x_vec)
    return data


def sphere_f(x):
    import numpy as np

    if x.__len__() == 3:
        center = np.array([4.0, 4.0, 4.0])
    elif x.__len__() == 2:
        center = np.array([4.0, 4.0])
    else:
        print "DIMENSION ERROR"
        quit()

    radius = 2.0
    d = x - center
    return np.dot(d, d) - radius ** 2


def torus_f(x):
    import numpy as np

    if x.__len__() == 3:
        center = np.array([4.0, 4.0, 4.0])
    elif x.__len__() == 2:
        center = np.array([4.0, 4.0])
    else:
        print "DIMENSION ERROR"
        quit()

    x=x-center
    R = 2.0
    r = 1.0
    return (np.dot(x,x)+R**2-r**2)**2-4*R**2*(x[0]**2+x[1]**2)


def doubletorus_f(x):
    import numpy as np

    if x.__len__() == 3:
        center = np.array([1.0, 4.0, 4.0])
    elif x.__len__() == 2:
        center = np.array([1.0, 4.0])
    else:
        print "DIMENSION ERROR"
        quit()

    x=(x-center)*1.0/2.0

    if x.__len__() == 2:
        return (x[0]*(x[0]-1)**2*(x[0]-2)+x[1]**2)**2-0.01
    else:
        return (x[0]*(x[0]-1)**2*(x[0]-2)+x[1]**2)**2-0.01+x[2]**2


def doubletorus_f_z(x):
    import numpy as np
    return doubletorus_f(np.array([x[0]-.5,x[1],x[2]-1]))


def doubletorus_f_y(x):
    import numpy as np
    return doubletorus_f(np.array([x[2]-.5,x[0]-1.5,x[1]]))


def doubletorus_f_x(x):
    import numpy as np
    return doubletorus_f(np.array([x[1],x[2]+2.5,x[0]-1.5]))


def normalize_resolution(old_data,old_res,old_dims):
    normalized_res = 1
    scaling_factor = normalized_res/old_res

    normalized_dims = {}
    for key,value in old_dims.items():
        normalized_dims[key] = scaling_factor*old_dims[key]

    normalized_data = {}
    for key,value in old_data.items():
        if old_data[key]<0:
            normalized_key = tuple(np.array(key) * scaling_factor)
            normalized_data[normalized_key] = -1
    print normalized_data
    return normalized_data, normalized_res, normalized_dims, scaling_factor


