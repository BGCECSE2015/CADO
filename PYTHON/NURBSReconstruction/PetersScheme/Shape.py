__author__ = 'erik + jc + anna'
# TODO: Merge Quad and Shape
import numpy as np

class Shape(object):
    def __init__(self, id, vertices):
        self._id = id
        self._vertices = vertices

    def get_vertices(self):
        return self._vertices

class Quad(Shape):
    # _quadlist and _vertexlist have to be of type np.array!
    def __init__(self, id, vertex1, vertex2, vertex3, vertex4, edge1, edge2, edge3, edge4):

        super(Quad, self).__init__(id, [vertex1, vertex2, vertex3, vertex4])
        #self._id = id
       # self._vertices = [vertex1, vertex2, vertex3, vertex4]
        for vertex in self._vertices:
            vertex.add_quad(self)

        self._edges = [edge1, edge2, edge3, edge4]
        for edge in self._edges:
            edge.add_quad(self)

    def get_vertices(self):
        return self._vertices

    def get_edges(self):
        return self._edges

    def get_opposite_vertex(self, vertex):
        vertex_index = self._vertices.index(vertex)
        opposite_index = (vertex_index + 2) % 4
        return self._vertices[opposite_index]

    def get_edge_neighbouring_quads(self):
        quad_list = []
        for edge in self._edges:
            for quad in edge.get_quads:
                if quad != self:
                    quad_list.append(quad)

        return quad_list

    def get_vertex_neighbouring_quads(self):
        quad_list = []
        for vertex in self._vertices:
            for quad in vertex.get_quads:
                if quad != self:
                    quad_list.append(quad)

        return

class Shape_DooSabin(Shape):
    # _quadlist and _vertexlist have to be of type np.array!
    def __init__(self, id, vertices):

        super(Shape_DooSabin, self).__init__(id, vertices)
        self.vertex_ids = np.array([self._vertices[i].getId() for i in range(len(self._vertices))])
        self.centroid = self.compute_centroid()
        #types can be: vertex, edge, center
        self.type = ""
        self.parent_type = ""
        self.parents = []
        #only for the faces which were generated from some vertex children
        self.parent_vertex = None
        self.edges = self.getEdges()
        self.parent_edge = None
        self.edge_face_positioning = None
        self.ordered_refined_vertices = [None]*16


    def compute_centroid(self):
        return np.mean([self._vertices[i]._coordinates for i in range(len(self._vertices))], 0)

    def getEdges(self):

        edges = []
        n = len(self._vertices)

        for i in range(n):
            edges.append([self._vertices[i], self._vertices[(i + 1) % n]])

        return edges

    def isAdjacent(self, face):
        face_edges = face.getEdges()
        flag = 0
        shared_edge = None
        for edge in self.getEdges():
            if (edge in face_edges) or ([edge[1], edge[0]] in face_edges):
                #flag = 1
                shared_edge = edge

        return shared_edge

    def adjacentEdges(self, vert):
        adjacent_edges = []
        for edge in self.getEdges():
            if vert in edge:
                adjacent_edges.append(edge)
        return adjacent_edges