__author__ = 'erik + jc + benni'
import numpy as np


class Coordinate(object):
    """
    Coordinate is a base class for everything which has a position.
    """
    def __init__(self, id, x, y, z):
        """
        :param id: id of this object
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        :return:
        """
        self._coordinates = np.array([x,y,z])
        self._id = id

    def get_id(self):
        """
        :return: id of this coordinate
        """
        return self._id

    def get_coordinates(self):
        """
        :return: numpy array holding the coordinates [x,y,z]
        """
        return self._coordinates


class Vertex(Coordinate):
    """
    A Vertex object is a part of a surface network. Therefore it is associated with Edges as well as Quads connected to
    this Vertex.
    """
    def __init__(self, id, x, y, z):
        """
        :param id: id of this vertex. The user has to take care, that this id is unique!
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        :return:
        """
        super(Vertex, self).__init__(id, x, y, z)
        self._edges = set()
        self._quads = set()

    def add_edge(self, edge):
        """
        adds an edge to the vertex. This means, that this edge is connected to the Vertex.
        :param edge: Edge object
        :return:
        """
        self._edges.add(edge)

    def add_quad(self, quad):
        """
        adds an quad to the vertex. This means, that this quad is connected to the Vertex
        :param quad: Quad object
        :return:
        """
        self._quads.add(quad)

    def get_edges(self):
        """
        :return: set of all edges connected to this Vertex
        """
        return self._edges

    def get_quads(self):
        """
        :return: set of all quads connected to this Vertex
        :rtype: PetersScheme.Edge
        """
        return self._quads

    def number_edges(self):
        """
        :return: number of edges connected to this vertex
        """
        return len(self._edges)

    def number_quads(self):
        """
        :return: number of quads connected to this vertex
        """
        return len(self._quads)

class FineVertex(Coordinate):
    """
    A FineVertex object is a vertex of the fine resolution representation of our surface reconstruction. Each of these
    vertices is associated with a Quad patch of the coarse resolution. Every FineVertex also has a set of parameters
    u and v, which corresponds to its parametrization in the parameter domain of the associated Quad.
    """
    def __init__(self, id, x, y, z, u, v, quad):
        """
        :param id: id of this vertex. The user has to take care, that this id is unique!
        :param x: x coordinate
        :param y: y coordinate
        :param z: z coordinate
        :param u: u parameter
        :param v: v parameter
        :param quad: associated Quad
        :return:
        """
        super(FineVertex, self).__init__(id, x, y, z)
        self._id = id
        self._quad = quad
        self._params = {'u':u, 'v':v}

    def get_parameters(self):
        """
        :return: the dict with both parameters u,v
        """
        return self._params

    def get_u(self):
        """
        :return: parameter u
        """
        return self._params['u']

    def get_v(self):
        """
        :return: parameter v
        """
        return self._params['v']

    def get_associated_quad(self):
        """
        Returns the pointer to the patch this FineVertex is associated with.
        :return: returns a Quad object
        """
        return self._quad


class Vertex_DooSabin(Vertex):
    def __init__(self, id, x, y, z):
     #   self._maltab_id = _id+1
        super(Vertex_DooSabin, self).__init__(id, x, y, z)
        self.neighbouringVertices = []
        self.neighbouringFaces = []
        self.childFace = None
        self.parentOrigGrid = None
        self.A = []
        self.B1 = []
        self.B2 = []
        self.C = []

    def getId(self):
        return self._id

    def getCoordinates(self):
        return self._coordinates

    def addNeighbouringVertex(self, vertex):
        #vertex should be of the type vertex!
        self.neighbouringVertices.append(vertex)
        return

    def addNeighbouringFace(self, face):
        #Face should be of the type face! Not a list of vertex ids
        self.neighbouringFaces.append(face)
        return
