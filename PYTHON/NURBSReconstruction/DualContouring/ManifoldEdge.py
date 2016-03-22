import numpy as np
from quadHelpers import quad_has_edge
from pColors import PColors

__author__ = 'benjamin'


class NonManifoldPointNotResolvedException(Exception):
    """
    is raised, if a point cannot be resolved
    """
    pass

class NonManifoldEdgeNotResolvedException(Exception):
    """
    is raised, if an edge cannot be resolved
    """
    pass


class ManifoldEdge:
    def __init__(self, _manifold_edge_key, _manifold_edge_quad_ids, _manifold_vertex_quad_ids_dict, _dc_vindex,
                 _dataset, _manifold_edge_set):
        # resolution of the grid
        self.resolution = _dataset._resolution

        # key corresponding to the vertices of the edge
        self.v_key = [None] * 2
        # indices corresponding to the vertices of the edge
        # access pattern v_idx[local_manifold_vertex_id] = global_vertex_id
        self.v_idx = _manifold_edge_key
        for i in range(2):
            self.v_key[i] = search_vertex_key_from_index(_dc_vindex, self.v_idx[i])

        # stores the indices of the child vertices of each manifold vertex after the edge is resolved
        # access pattern: v_children_idx[local_manifold_vertex_id][split_id] = global_vertex_id
        self.v_children_idx = [2 * [None] for _ in range(2)]

        # stores the edge keys of edges connected to the respective children after the edge is resolved
        # access pattern: v_children_edge_keys[local_manifold_vertex_id][split_id] = list of connected vertices
        self.v_children_connection_idx = [[[] for _ in range(2)] for _ in range(2)]

        # direction vector of the edge (direction vertex0 -> vertex1) and corresponding dimensions
        self.edge_dir01, self.edge_dim = self.calculate_edge_dir01()

        # keys of neighbouring voxels and the directions
        self.neighbour_keys, self.neighbour_directions = self.calculate_neighbour_keys()

        # key of the datavalue at the middle of the face penetrated by the edge and the index [0] or [1] of the v_key
        # lying in that plane
        self.middle_value_key, self.middle_plane_index = self.calculate_middle_value_key()
        # datavalue at middle_value_key
        self.middle_sign = self.calculate_middle_sign(_dataset)
        # quad indices of quads connected to this edge with an edge
        self.manifold_edge_quads_ids = _manifold_edge_quad_ids
        # quad indices of quads connected to this edge with a vertex
        self.manifold_vertex_quad_ids = 2 * [None]
        self.manifold_vertex_quad_ids[0] = _manifold_vertex_quad_ids_dict[self.v_idx[0]]
        self.manifold_vertex_quad_ids[1] = _manifold_vertex_quad_ids_dict[self.v_idx[1]]

        # kind of the vertex.
        # A vertex is either connected to the outside of the volume or to the inside (hybrid configurations and
        # connections to other manifold edges are also possible!)
        self.v_kind = [None] * 2
        for local_v_idx in range(2):
            self.v_kind[local_v_idx] = self.determine_kind_of_vertex(local_v_idx, _dataset, _manifold_edge_set)

    def determine_kind_of_vertex(self, _local_v_idx, _dataset, _manifold_edge_set):

        # 1.    is the vertex connected to another manifold edge?
        #       check references by other manifold edges!
        other_manifold_edges = list(sorted(_manifold_edge_set))
        other_manifold_edges.remove(tuple(sorted(self.v_idx)))
        other_manifold_edges = np.array(other_manifold_edges)

        if self.v_idx[_local_v_idx] in other_manifold_edges:
            return "manifold"

        # 2.    is the vertex connected to the outside or inside plane?
        #       go some further steps in manifold edge direction and evaluate data!
        if _local_v_idx == 0:
            edge_dir_value_key = tuple(np.array(self.middle_value_key) + self.resolution * self.edge_dir01)
        elif _local_v_idx == 1:
            edge_dir_value_key = tuple(np.array(self.middle_value_key) - self.resolution * self.edge_dir01)
        else:
            print "dc3D - determine_kind_of_vertex: UNDEFINED INDEX!"
            quit()

        edge_dir_perpendicular = 4 * [np.array([0, 0, 0])]
        idx = 0
        for d in range(3):
            if d != self.edge_dim:
                for value in [-1, 1]:
                    edge_dir_perpendicular[idx][d] = value
                    idx += 1

        perp_signs = 4 * [None]  # check the four signs perpendicular to the edge direction
        for idx in range(4):
            edge_dir_perpendicular_key = tuple(
                np.array(edge_dir_value_key) + self.resolution * edge_dir_perpendicular[idx])
            perp_signs[idx] = _dataset[edge_dir_perpendicular_key]
            edge_dir_sign = _dataset[edge_dir_value_key]

        if not edge_dir_sign:
            return "outside"  # (3.)
        else:
            return "inside"  # (3.)

        return "hybrid"  # (2.)

    def calculate_middle_sign(self, _dataset):
        key = self.middle_value_key
        return _dataset[key]

    def calculate_edge_dir01(self):
        v_o = [None] * 2
        # v_o describes the origin of the respective voxel
        for i in range(2):
            v_o[i] = np.array(self.v_key[i])

        edge_dir01 = v_o[0] - v_o[1]
        edge_dir01 /= np.linalg.norm(edge_dir01)
        edge_dim = np.where(np.abs(edge_dir01) == 1)[0][0]

        return edge_dir01, edge_dim

    def calculate_middle_value_key(self):
        displacement = np.array([1.0, 1.0, 1.0]) * self.resolution / 2
        displacement[self.edge_dim] = 0.0
        if self.v_key[0][self.edge_dim] > self.v_key[1][self.edge_dim]:  # v_key[0] is in the plane crossed by the edge
            middle_plane_idx = 0
            return tuple(np.array(self.v_key[0]) + displacement), middle_plane_idx
        else:  # v_key[1] is in that plane
            middle_plane_idx = 1
            return tuple(np.array(self.v_key[1]) + displacement), middle_plane_idx

    def calculate_neighbour_keys(self):

        neighbor_directions = []

        for d in range(3):
            if d != self.edge_dim:
                for j in [-1, 1]:
                    neighbor_direction = np.zeros(3)
                    neighbor_direction[d] = j
                    neighbor_directions.append(neighbor_direction)

        neighbor_keys = 2 * [4 * [None]]
        for i in range(2):
            for j in range(4):
                neighbor_keys[i][j] = tuple(np.array(self.v_key[i]) + self.resolution * neighbor_directions[j])

        return neighbor_keys, neighbor_directions

    def resolve(self, _dataset, _vindex, _dc_quads, _dc_verts, o_idx_nodes, vindex_mapping):
        new_quads_list = []  # new quads contributed by this edge are stored here
        new_nodes_list = []  # new nodes introduced by manifold edge splitting are stored here
        delete_quads_list = self.manifold_edge_quads_ids  # the old quads connected to the manifold edge are deleted in any case!
        child_id = 0  # this will be incremented, after we have added an edge
        o_idx_shift = 0
        # we need to resolve the ambiguous cases: break or join surface with the new quads? Therefore we traverse all
        # the nodes in the same plane as the middle value
        for neighbour_pair_key in [(0, 2), (0, 3), (1, 2), (1, 3)]:  # create new quads and remove manifold quads
            # direction of the current node
            sign_direction = np.array(self.neighbour_directions[neighbour_pair_key[0]]) \
                             + np.array(self.neighbour_directions[neighbour_pair_key[1]])
            # key of the node
            sign_key = tuple(np.array(self.middle_value_key) + self.resolution * .5 * sign_direction)
            # value of the node
            sign = _dataset.value_at(sign_key)

            # resolves ambiguous case: if sign is equal to middle sign, we don't want to create a quad in between, which
            # separates the two nodes. If the signs are not equal, we want to separate them with two new quads
            if sign != self.middle_sign:
                new_quads = 2 * [None]  # init two quads

                # initialize new edge, the quads will be connected to instead of manifold edge
                normal_direction = sign_direction * self.resolution * 1.0 / 4.0  # the normal is in the direction of the sign
                for m_v_id in range(2):  # we will have to copy the manifold edge and shift it
                    if (self.v_idx[m_v_id], child_id) in vindex_mapping:
                        node_idx = vindex_mapping[(self.v_idx[m_v_id], child_id)]
                    else:
                        new_nodes_list.append(
                            _dc_verts[self.v_idx[m_v_id]] + normal_direction)  # shift new nodes into normal direction
                        node_idx = o_idx_nodes + o_idx_shift
                        o_idx_shift += 1
                        vindex_mapping[(self.v_idx[m_v_id], child_id)] = node_idx
                    self.v_children_idx[m_v_id][child_id] = node_idx  # store global index of this node in object

                # each edge is parallel to the manifold edge, but shifted in the direction of one of the two neighbours
                for edge_id in range(2):
                    v_ids = 2 * [None]  # find global neighbour vertex indices
                    for v_id in range(2):  # calculate ids of both vertices of the neighbouring edge
                        v_key = tuple(np.array(self.v_key[v_id])
                                      + self.resolution * self.neighbour_directions[neighbour_pair_key[edge_id]])
                        v_ids[v_id] = _vindex[v_key]

                    # calculate corresponding edge key
                    manifold_edge_key = tuple(sorted(tuple(v_ids)))

                    # find quad which contains this edge
                    for local_q_id in range(4):
                        quad = _dc_quads[self.manifold_edge_quads_ids[local_q_id]]

                        if quad_has_edge(quad, manifold_edge_key):
                            new_quads[edge_id] = list(quad)  # copy quad

                            # swap both references to manifold edge with reference to newly created node
                            for m_v_id in range(2):
                                tmp = new_quads[edge_id].index(
                                    self.v_idx[m_v_id])  # find reference to node of manifold edge
                                new_quads[edge_id][tmp] = self.v_children_idx[m_v_id][
                                    child_id]  # replace with reference to new node
                                for shift in [-1, +1]:
                                    neighbour_idx = quad[(tmp + shift) % 4]
                                    if neighbour_idx != self.v_idx[int(not m_v_id)]:
                                        self.v_children_connection_idx[m_v_id][child_id].append(neighbour_idx)

                            # only one quad out of self.manifold_edge_quads is connected to this neighbouring edge
                            break

                new_quads_list += new_quads  # append 2 new quads to new_quads_list
                child_id += 1  # incrementing child id


                #############################################
                # child of original manifold edge processes #
                #############################################

        ##########################
        # all children processed #
        ##########################

        # change remaining references to removed edge -> treat vertices!
        # this depends on the self.v_kind of the vertex!

        o_idx_return = o_idx_nodes + o_idx_shift
        for i in range(2):
            try:
                kind = self.v_kind[i]
                if kind == "outside":
                    new_quads, new_nodes, delete_quads, o_idx_return = self.resolve_outside_vertex(i, _dc_quads,
                                                                                                   _dc_verts,
                                                                                                   o_idx_return)
                elif kind == "inside":
                    new_quads, delete_quads = self.resolve_inside_vertex(i, _dc_quads)
                    new_nodes = []
                elif kind == "manifold":  # manifold vertices do not have to be treaten separately!
                    new_quads = []
                    new_nodes = []
                    delete_quads = []
                else:
                    print "unknown type! aborting..."
                    quit()
                new_nodes_list += new_nodes
                new_quads_list += new_quads
                delete_quads_list += delete_quads
            except NonManifoldPointNotResolvedException as e:
                import traceback, os.path
                top = traceback.extract_stack()[-1]
                print ''
                print ', '.join([os.path.basename(top[0]), str(top[1])])
                print PColors.WARNING + "One of the non manifold points wasn't resolved correctly. WHOLE EDGE NOT RESOLVED!" + PColors.ENDC + "\n"
                raise NonManifoldEdgeNotResolvedException("Edge not resolved!")
                new_nodes_list = []
                new_quads_list = []
                delete_quads_list = []
                o_idx_return = o_idx_nodes + o_idx_shift

        return new_quads_list, new_nodes_list, delete_quads_list, o_idx_return, vindex_mapping

    def resolve_outside_vertex(self, _local_v_id, _dc_quads, _dc_verts, o_idx_nodes):
        new_quads_list = []
        new_nodes_list = []
        neighbour_quads = self.manifold_vertex_quad_ids[_local_v_id]

        midpoint_idx = self.v_idx[_local_v_id]

        if neighbour_quads.__len__() == 2:  # flat outside
            for i in range(2):
                # all quads connected to the vertex will be deleted
                delete_quads_list = neighbour_quads
                quad = _dc_quads[neighbour_quads[i]]
                tmp = quad.index(midpoint_idx)
                for shift in [-1, +1]:
                    pivot = quad[(tmp + shift) % 4]
                    opposite = quad[(tmp + 2) % 4]

                    new_quad = [midpoint_idx]

                    if pivot in self.v_children_connection_idx[_local_v_id][0]:
                        new_quad.append(self.v_children_idx[_local_v_id][0])
                    elif pivot in self.v_children_connection_idx[_local_v_id][1]:
                        new_quad.append(self.v_children_idx[_local_v_id][1])
                    else:
                        print "resolve_outside_vertex: unexpected case!"
                        quit()

                    new_quad += [pivot, opposite]
                    new_quads_list.append(new_quad)

        elif neighbour_quads.__len__() == 3:  # L-shape
            # find neighbouring quad lying in the plane
            for q_id in neighbour_quads:
                quad = _dc_quads[q_id]

                checker = 2 * [None]
                connection_chooser = 2 * [None]

                for child_id in range(2):
                    for conn_id in range(2):
                        if self.v_children_connection_idx[_local_v_id][child_id][conn_id] in quad:
                            checker[child_id] = True
                            connection_chooser[child_id] = conn_id
                            break

                if all(checker):
                    quad_plane_id = q_id
                    quad_plane = quad
                    break

            try:
                assert 'quad_plane' in locals()
            except AssertionError as e:
                import traceback, os.path
                top = traceback.extract_stack()[-1]
                print '\n'
                print ', '.join([os.path.basename(top[0]), str(top[1])])
                new_quads_list = []
                new_nodes_list = []
                delete_quads_list = []
                raise NonManifoldPointNotResolvedException("EDGE NOT RESOLVED! EXCEPTION UNCAUGHT!")
                print PColors.WARNING + "One non-manifold edge is not resolved in the correct way." + PColors.ENDC + '\n'
                return new_quads_list, new_nodes_list, delete_quads_list, o_idx_nodes


            # add four new quads and one new point
            centroid = np.zeros([3])
            for v_idx in quad_plane:
                centroid += _dc_verts[v_idx]
            centroid /= 4.0
            new_node = centroid

            midpoint_idx = self.v_idx[_local_v_id]
            opposite_idx = quad_plane[(quad_plane.index(midpoint_idx) + 2) % 4]

            for child_id in range(2):
                child_ids = self.v_children_idx[_local_v_id]
                child_connections = self.v_children_connection_idx[_local_v_id][child_id]
                new_quad = [midpoint_idx,
                            child_connections[connection_chooser[int(not child_id)]],
                            child_ids[child_id],
                            o_idx_nodes]
                new_quads_list.append(new_quad)

                new_quad = [child_ids[child_id],
                            child_connections[connection_chooser[child_id]],
                            opposite_idx,
                            o_idx_nodes]
                new_quads_list.append(new_quad)

            # one quads will be deleted
            delete_quads_list = [quad_plane_id]
            o_idx_nodes += 1
            new_nodes_list = [new_node]

        else:  # unknown shape!
            print "not treated properly!"
            delete_quads_list = []

        return new_quads_list, new_nodes_list, delete_quads_list, o_idx_nodes

    def resolve_inside_vertex(self, _local_v_id, _dc_quads):
        # all quads connected to the vertex will be removed anyhow
        delete_quads_list = self.manifold_vertex_quad_ids[_local_v_id]
        new_quads_list = []

        # change all references to old manifold vertex to references to the right child vertex

        for q_id in delete_quads_list:
            quad = _dc_quads[q_id]
            tmp = quad.index(self.v_idx[_local_v_id])
            new_quad = list(quad)

            for child_id in range(2):
                if np.intersect1d(quad, self.v_children_connection_idx[_local_v_id][child_id]).__len__() != 0:
                    new_quad[tmp] = self.v_children_idx[_local_v_id][child_id]
                    break

            new_quads_list.append(new_quad)

        return new_quads_list, delete_quads_list

    def resolve_manifold_vertex(self, _local_v_id, _dc_quads):
        # all quads connected to the vertex will be removed anyhow
        delete_quads = list(self.manifold_vertex_quad_ids[self.v_idx[_local_v_id]])
        # no new quads are generated!
        new_quad = []

        return new_quad, delete_quads


# searches the corresponding key with a given vertex index
def search_vertex_key_from_index(_dc_vindex, idx):
    for key in _dc_vindex:
        if int(_dc_vindex[key]) == int(idx):
            return key
    raise Exception("ERROR! INDEX %d not found" % idx)
