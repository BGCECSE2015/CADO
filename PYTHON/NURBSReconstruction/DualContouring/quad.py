__author__ = 'benjamin'


class Quad:
    # _quadlist and _vertexlist have to be of type np.array!
    def __init__(self, _id, _quadlist, _vertexlist):
        import numpy as np
        if type(_quadlist) is list:
            _quadlist = np.array(_quadlist)
        if type(_vertexlist) is list:
            _vertexlist = np.array(_vertexlist)

        if not (type(_quadlist) is np.ndarray and type(_vertexlist) is np.ndarray):
            raise Exception("WRONG TYPE! exiting...")

        self.quad_id = _id
        self.vertex_ids = _quadlist[_id]
        self.centroid = self.compute_centroid(_vertexlist)
        self.is_plane = self.compute_plane(_vertexlist)
        self.normal = self.compute_normal(_vertexlist)
        self.vertices_plane = self.compute_plane_corner_points(_vertexlist)
        self.ortho_basis_AB, \
        self.basis_BAD, \
        self.ortho_basis_CB, \
        self.basis_BCD = \
            self.compute_basis(_vertexlist)# [edge_AB;edge_orthogonal;normal]

        self.neighbors = self.find_neighbors(_quadlist)
        #self.basis, self.basis_inv = self.get_basis()

    def compute_centroid(self, _vertexlist):
        import numpy as np
        return np.mean(_vertexlist[self.vertex_ids],0)

    def compute_plane(self, _vertexlist):
        import numpy as np

        A=_vertexlist[self.vertex_ids[0]]
        B=_vertexlist[self.vertex_ids[1]]
        C=_vertexlist[self.vertex_ids[2]]
        D=_vertexlist[self.vertex_ids[3]]

        AB=B-A
        AC=C-A
        AD=D-A

        Q=np.array([AB,AC,AD])

        return abs(np.linalg.det(Q))<10**-14

    def compute_normal(self, _vertexlist):
        import numpy as np

        if self.is_plane:
            vertex1 = _vertexlist[self.vertex_ids[1]]
            vertex2 = _vertexlist[self.vertex_ids[2]]
            vertex3 = _vertexlist[self.vertex_ids[3]]

            edge12 = vertex2-vertex1
            edge13 = vertex3-vertex1

            normal = np.cross(edge12,edge13)
            normal /= np.linalg.norm(normal)

        else:
            #find least squares fit plane
            lsq_matrix = _vertexlist[self.vertex_ids] - self.centroid
            u, s, v = np.linalg.svd(lsq_matrix)
            idx = np.where(np.min(abs(s)) == abs(s))[0][0]

            normal = v[idx, :]
            normal /= np.linalg.norm(normal)

        return normal

    # TODO there is a problem with the coordinate system of the quad:
    # One system is right handed, one left. In the end the parameters are therefore flipped. For now we fixed this in a
    # quite pragmatic way, but it should be improved in a refactoring session!
    def compute_basis(self, _vertexlist):
        import numpy as np

        vertexA = self.vertices_plane[0,:]
        vertexB = self.vertices_plane[1,:]
        vertexC = self.vertices_plane[2,:]
        vertexD = self.vertices_plane[3,:]
        edgeAB = vertexB - vertexA
        edgeAD = vertexD - vertexA
        edgeCB = vertexB - vertexC
        edgeCD = vertexD - vertexC

        basis_BAD = np.array([self.normal, edgeAB, edgeAD])
        basis_BCD = np.array([self.normal, edgeCD, edgeCB])

        edgeAB_normalized = edgeAB / np.linalg.norm(edgeAB)
        edgeCD_normalized = edgeCD / np.linalg.norm(edgeCD)

        ortho_basis_AB = np.array([self.normal,
                                   edgeAB_normalized,
                                   np.cross(edgeAB_normalized, self.normal)])
        ortho_basis_CD = np.array([self.normal,
                                   edgeCD_normalized,
                                   np.cross(edgeCD_normalized, self.normal)])

        return ortho_basis_AB.transpose(), basis_BAD.transpose(), ortho_basis_CD.transpose(), basis_BCD.transpose()

    def projection_onto_plane(self, _point):
        import numpy as np

        distance = np.dot(self.centroid-_point, self.normal)
        projected_point = _point+distance*self.normal
        return projected_point, distance

    def point_on_quad(self, u, v):
        import numpy as np

        if u+v <= 1 and u >= 0 and v >= 0:
            vertexA = self.vertices_plane[0,:]
            point = vertexA + np.dot(self.basis_BAD[:,1:3],[u,v])

        elif u+v > 1 >= u and v <= 1:
            vertexC = self.vertices_plane[2,:]
            u = -u+1
            v = -v+1
            point = vertexC + np.dot(self.basis_BCD[:,1:3],[u,v])

        else:
            print "INVALID INPUT!"
            quit()

        return point

    def projection_onto_quad(self, _point):
        from scipy.linalg import solve_triangular
        import numpy as np

        # first assume that _point is below diagonal BD
        vertexA = self.vertices_plane[0,:]
        vector_vertexA_point = _point - vertexA
        # we want to transform _point to the BASIS=[normal,AB,AC] and use QR decomposition of BASIS = Q*R
        # BASIS * coords = _point -> R * coords = Q' * _point
        R_BAD = np.dot(self.ortho_basis_AB.transpose(),self.basis_BAD)
        b = np.dot(self.ortho_basis_AB.transpose(),vector_vertexA_point)
        x = solve_triangular(R_BAD,b)
        distance = x[0]
        projected_point = _point - distance * self.normal
        u = x[1]
        v = x[2]

        # if not, _point is above diagonal BD
        if u+v > 1:
            vertexC = self.vertices_plane[2,:]
            vector_vertexC_point = _point - vertexC
            R_BCD = np.dot(self.ortho_basis_CB.transpose(),self.basis_BCD)
            b = np.dot(self.ortho_basis_CB.transpose(),vector_vertexC_point)
            x = solve_triangular(R_BCD,b)
            distance = x[0]
            projected_point = _point - distance * self.normal
            u = 1-x[1]
            v = 1-x[2]

        distance = abs(distance)

        u_crop = u
        v_crop = v

        if not (0<=u<=1 and 0<=v<=1):
            if u < 0:
                u_crop = 0
            elif u > 1:
                u_crop = 1

            if v < 0:
                v_crop = 0
            elif v > 1:
                v_crop = 1

            projected_point = self.point_on_quad(u_crop,v_crop)
            distance = np.linalg.norm(_point-projected_point)

        return projected_point, distance, u, v

    def measure_centroid_distance_squared(self, _point):
        import numpy as np

        r = self.centroid-_point
        return np.dot(r,r)

    def compute_plane_corner_points(self, _vertexlist):
        import numpy as np

        if self.is_plane:
            return _vertexlist[self.vertex_ids]
        else:
            #return corner points projected onto fit plane!
            vertices = _vertexlist[self.vertex_ids]
            projected_vertices = np.zeros([4,3])
            i = 0
            for vertex in vertices:
                projected_vertex, distance = self.projection_onto_plane(vertex)
                projected_vertices[i,:] = projected_vertex
                i += 1

            return projected_vertices

    def find_neighbors(self,_quadlist):
        import numpy as np

        neighbors = np.array([])

        edges = [self.vertex_ids[[0,1]],
                 self.vertex_ids[[1,2]],
                 self.vertex_ids[[2,3]],
                 self.vertex_ids[[3,0]]]

        for e in edges:
            has_vertex1 = np.where(_quadlist == e[0])[0]
            has_vertex2 = np.where(_quadlist == e[1])[0]
            same_edge = np.intersect1d(has_vertex1, has_vertex2)
            neighbor = same_edge[same_edge != self.quad_id]
            neighbors = np.append(neighbors, neighbor)

        return neighbors.astype(int)