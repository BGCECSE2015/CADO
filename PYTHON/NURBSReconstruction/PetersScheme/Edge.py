__author__ = 'erik + jc'


class Edge:
    def __init__(self, id, vertex1, vertex2):

        self._id = id
        self._vertices = set([vertex1, vertex2])
        for vertex in self._vertices:
            vertex.add_edge(self)

        self._quads = set()

    def add_quad(self, quad):
        self._quads.add(quad)

    def get_vertices(self):
        return self._vertices

    def get_quads(self):
        return self._quads

    def get_other_vertex(self, vertex):
        for vertex_test in self._vertices:
            if vertex_test is not vertex:
                return vertex_test


    def number_quads(self):
        """
        :return: number of quads connected to this edge (should always be equal to 2!)
        """
        return len(self._quads)