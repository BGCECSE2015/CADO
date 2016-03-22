import itertools as it
import numpy as np
from vtk_parsing import parse_file_vtk


def voxel(edge_length, center):
    """
    returns the data which is needed for plotting the faces of one voxel (a cube)
    :param edge_length: edge length of the cube
    :param center: center of gravity of the cube
    :return: list with list containing the four vertices of the six faces of the cube
    """
    center = np.array(center)
    scale = 1
    x0 = (center + edge_length * scale * .5 * np.array([-1, -1, -1])).tolist()
    x1 = (center + edge_length * scale * .5 * np.array([-1, 1, -1])).tolist()
    x2 = (center + edge_length * scale * .5 * np.array([1, 1, -1])).tolist()
    x3 = (center + edge_length * scale * .5 * np.array([1, -1, -1])).tolist()
    x4 = (center + edge_length * scale * .5 * np.array([-1, -1, 1])).tolist()
    x5 = (center + edge_length * scale * .5 * np.array([-1, 1, 1])).tolist()
    x6 = (center + edge_length * scale * .5 * np.array([1, 1, 1])).tolist()
    x7 = (center + edge_length * scale * .5 * np.array([1, -1, 1])).tolist()

    return [[x0, x1, x2, x3, x0],
            [x4, x5, x6, x7, x4],
            [x0, x1, x5, x4, x0],
            [x2, x3, x7, x6, x2],
            [x0, x3, x7, x4, x0],
            [x1, x2, x6, x5, x1]]


def parse_dims(dims, res):
    """
    parses the dimensions in the correct format for the VoxelDataset object
    :param dims: dimensions
    :param res: resolution
    :return:
    """
    if dims.__len__() == 6:
        dims_return = {'min': 3 * [None], 'max': 3 * [None]}
        dims_return['min'][0] = dims['xmin']
        dims_return['min'][1] = dims['ymin']
        dims_return['min'][2] = dims['zmin']
        dims_return['max'][0] = dims['xmax']
        dims_return['max'][1] = dims['ymax']
        dims_return['max'][2] = dims['zmax']
    elif dims.__len__() == 2:
        dims_return = dims
    else:
        raise Exception("dims has wrong length!")

    for d in range(3):  # check if dimensions match with resolution
        gap = (dims_return['max'][d] - dims_return['min'][d]) % res  # if dimensions match, this is equal to 0!
        dims_return['max'][d] += (res - gap) % res

    return dims_return


def parse_data(data):
    """
    parses the data in the correct format for the VoxelDataset object.
    :param data: data might have a different format (e.g. dict)
    :return: a set containing all the points which lie inside the geometry
    """
    if type(data) is set:
        return_data = data
    elif type(data) is dict:
        return_data = set()
        for key, value in data.items():
            if value == -1:
                return_data.add(key)
    else:
        raise Exception("data of wrong type!")

    return return_data


class VoxelDataset():
    """
    Object which has a dataset containing inside/outside information along with the dimensionality of the bounding box
    and the spacing of the gridpoints. The inside/outside information is stored on a uniform grid and represented by a
    set containing those points which are inside. Some additional data (not on the uniform grid) might be in the set,
    which is needed for ambiguity resolution.
    """
    def __init__(self, dims, resolution, data):
        """
        constructor called with dict or set data
        :param dims:
        :param resolution:
        :param data:
        :return:
        """
        assert type(dims) is dict
        self._dimensions = parse_dims(dims, resolution)

        assert type(resolution) is int
        assert resolution >= 1
        self._resolution = int(resolution)

        self._data = parse_data(data)

    @classmethod
    def from_filename(cls, filepath):
        """
        constructor called with a filepath to a csv holding a vector of cell data
        :param filepath:
        :return:
        """

        dims_from_file, origin_from_file, spacing_from_file, points_from_file = parse_file_vtk(filename=filepath)
        dims = {'min':3*[None], 'max':3*[None]}
        res = int(spacing_from_file[0])

        for d in range(3):
            assert spacing_from_file[d] == res
            dims['min'][d] = origin_from_file[d]
            dims['max'][d] = spacing_from_file[d] * dims_from_file[d] + origin_from_file[d]

        data_matrix = np.array(points_from_file,dtype=bool).reshape(dims_from_file,order='F')

        data = set()
        for i in range(data_matrix.shape[0]):
            for j in range(data_matrix.shape[1]):
                for k in range(data_matrix.shape[2]):
                    if data_matrix[i,j,k]:
                        key = tuple(origin_from_file + np.array([i,j,k]) * spacing_from_file)
                        data.add(key)

        return cls(dims,res,data)

    def align(self):
        """
        Aligns the dataset to integer values. Assumes, that the resolution is equal to 1. Non integer points are just
        cropped.
        """

        # align dimensions
        aligned_dims={'min':3*[None],'max':3*[None]}
        for d in range(3):
            aligned_dims['min'][d] = np.floor(self._dimensions['min'][d])
            aligned_dims['max'][d] = np.floor(self._dimensions['max'][d])

        # align data
        aligned_data = set()
        aligned_key = np.zeros(3)
        for key in self._data:
            for d in range(3):
                aligned_key[d] = np.floor(key[d])
            aligned_data.add(tuple(aligned_key))


        # overwrite old dataset and dimensions
        self._data = aligned_data
        self._dimensions = aligned_dims

    def surround(self):
        """
        surrounds the dataset with outside data values by extending dimensions by one layer
        :return:
        """
        for d in range(3):
            self._dimensions['min'][d] = self._dimensions['min'][d] - self._resolution
            self._dimensions['max'][d] = self._dimensions['max'][d] + self._resolution


    def point_is_inside(self, point):
        """
        Checks whether a point is inside the bounding box.
        :param point: point for which we want to get information
        :return: boolean value
        """
        assert type(point) is tuple
        assert point.__len__() == 3

        for d in range(3):
            if not (self._dimensions['min'][d] <= point[d] <= self._dimensions['max'][d]):
                # point is in one dimensions not inside
                return False
        # point is in all dimensions inside bounding box
        return True

    def point_is_aligned(self, point):
        """
        Checks if the point is aligned to the uniform grid defined by self._dimensions and self._resolution.
        :param point:
        :return:
        """
        assert type(point) is tuple
        assert point.__len__() == 3

        for d in range(3):
            if (abs(point[d] - self._dimensions['min'][d]) % (self._resolution * .5)) != 0:  # point is not aligned
                return False
        # all points are obviously aligned
        return True

    def valid_point(self, point):
        """
        Checks if the point is valid. This means if it is lying inside the bounding box defined by self._dimensions
        :param point:
        :return:
        """
        assert type(point) is tuple
        assert point.__len__() == 3

        if not self.point_is_inside(point):
            return False
        else:
            return True

    def value_at(self, point):
        """
        Checks whether a point is an inside point. Only points, which are contained in self._dataset are inside. All
        other points are defined as outside (Therefore, one should only iterate over the uniform grid!).
        :param point:
        :return:
        """
        return self._value_at_wo_checks(point)

    def _value_at_w_checks(self, point):
        if self.valid_point(point):
            return point in self._data
        else:
            if not self.point_is_inside(point):
                raise Exception("invalid point! Point %s is not inside %s." % (point, self._dimensions))

    def _value_at_wo_checks(self, point):
        return point in self._data

    def __getitem__(self, item):
        assert type(item) is tuple
        assert item.__len__() == 3
        return self.value_at(item)

    def get_grid_iterator(self):
        """
        :return: Iterator for the uniform grid of the dataset.
        """
        return it.product(np.arange(self._dimensions['min'][0], self._dimensions['max'][0], self._resolution),
                          np.arange(self._dimensions['min'][1], self._dimensions['max'][1], self._resolution),
                          np.arange(self._dimensions['min'][2], self._dimensions['max'][2], self._resolution))

    def get_total_voxels(self):
        """
        :return: Total number of voxels covered by this dataset
        """
        return np.arange(self._dimensions['min'][0], self._dimensions['max'][0], self._resolution).__len__() * \
               np.arange(self._dimensions['min'][1], self._dimensions['max'][1], self._resolution).__len__() * \
               np.arange(self._dimensions['min'][2], self._dimensions['max'][2], self._resolution).__len__()


    def plot(self, axis, color, alpha):
        """
        Plots the whole dataset to the given axis. Only inside voxels are plotted and represented by cubes.
        :param axis: axis where we draw the plot
        :param color: color of the cubes
        :param alpha: alpha value, if alpha is 0 just the edges of the cubes are drawn
        """
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
        for x, y, z in self.get_grid_iterator():
            key = (x, y, z)
            if key in self._data:
                voxel_data = voxel(edge_length=self._resolution, center=key)
                if alpha != 0:
                    vox = Poly3DCollection(voxel_data)
                    vox.set_color(color)
                    vox.set_alpha(alpha)
                    vox.set_edgecolor('k')
                    axis.add_collection3d(vox)
                else:
                    mesh = Line3DCollection(voxel_data,colors=color)
                    axis.add_collection3d(mesh)