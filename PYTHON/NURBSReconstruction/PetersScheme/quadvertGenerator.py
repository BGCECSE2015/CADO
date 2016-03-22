__author__ = 'juan'
import numpy as np
from Vertex import Vertex, FineVertex
from Edge import Edge
from Quad import Quad


def quad_vert_generator(_verts, _quads, _fine_verts, _parameters ):
    assert type(_verts) is np.ndarray
    assert type(_quads) is np.ndarray
    assert type(_fine_verts) is np.ndarray
    # Create vertices
    vertex_list = []
    for i in range(_verts.shape[0]):
        vertex_list.append(Vertex(id=i, x=_verts[i, 0], y=_verts[i, 1], z=_verts[i, 2]))

    # Creating edges
    edge_dict = {}
    edge_id = 0
    for i in range(_quads.shape[0]):
        edges = [(_quads[i, 0], _quads[i, 1]),  # edges of this quad
                 (_quads[i, 1], _quads[i, 2]),
                 (_quads[i, 2], _quads[i, 3]),
                 (_quads[i, 3], _quads[i, 0])]
        for e in edges:
            key = tuple(sorted(e))
            if key not in edge_dict:
                edge_dict[key] = Edge(edge_id, vertex_list[int(key[0])], vertex_list[int(key[1])])
                edge_id += 1

    # Creating quads
    quad_list = []
    for i in range(_quads.shape[0]):
        a = int(_quads[i, 0])
        b = int(_quads[i, 1])
        c = int(_quads[i, 2])
        d = int(_quads[i, 3])
        e1 = tuple(sorted([_quads[i, 0], _quads[i, 1]]))  # edges of this quad
        e2 = tuple(sorted((_quads[i, 1], _quads[i, 2])))
        e3 = tuple(sorted((_quads[i, 2], _quads[i, 3])))
        e4 = tuple(sorted((_quads[i, 3], _quads[i, 0])))
        quad_list.append(Quad(i, vertex_list[a], vertex_list[b], vertex_list[c], vertex_list[d],
                         edge_dict[e1], edge_dict[e2], edge_dict[e3], edge_dict[e4]))

    # Erasing hanging nodes
    for i in range(vertex_list.__len__()):
        if not vertex_list[i].get_quads():
            if vertex_list[i].get_edges():
                print "ERROR, hanging vertex with edges"

            vertex_list[i] = None


    # New Id's of vertices
    new_id = 0
    new_vertex_list = []
    for i in range(vertex_list.__len__()):
        if vertex_list[i] is not None:
            vertex_list[i]._id = new_id
            new_vertex_list.append(vertex_list[i])
            new_id += 1

    # Check if every edge has only two quads!
    for e in edge_dict:
        if edge_dict[e].get_quads().__len__() > 2:
            print e
    # Create fine vertices
    fine_vertex_list = []

    for i in range(_fine_verts.shape[0]):
        fine_vertex_list.append(FineVertex(id=i, x=_fine_verts[i, 0], y=_fine_verts[i, 1], z=_fine_verts[i, 2],
                                u=_parameters[i, 1], v=_parameters[i, 2], quad=quad_list[int(_parameters[i, 0])]))
    verts=[]

    quads=[]

    verts= [new_vertex_list[i].get_coordinates()  for i in range(new_vertex_list.__len__())]
    fine_verts= [fine_vertex_list[i].get_coordinates()  for i in range(fine_vertex_list.__len__())]

    for i in range(quad_list.__len__()):
        quads.append([quad_list[i].get_vertices()[j].get_id() for j in range(4)])

    return np.array(verts), np.array(quads), np.array(fine_verts), new_vertex_list, edge_dict, quad_list
















