__author__ = 'erik'
import numpy as np

from PetersScheme.Edge import Edge
from PetersScheme.Quad import Quad
from PetersScheme.Vertex import Vertex


def getABsC_ind(quadIndex, indVertex, indOtherVertex, regularPoints):
    '''
    :param _quad:
    :param indVertex:
    :param indOtherVertex:
    :param regularPoints:
    :return:
    '''
    assert isinstance(quadIndex,int)
    assert isinstance(indVertex,int)
    assert isinstance(indOtherVertex,int)
    assert isinstance(regularPoints,np.ndarray)

    # assuming 16 vertices per row of regularPoints
    # listed like
    '''

    4-------------------2
    |   12  13  14  15  |
    |   8   9   10  11  |
    |   4   5   6   7   |
    |   0   1   2   3   |
    0-------------------1

    '''
    # points in order A, B1, B2, C
    # B1 is the one closest to the edge
    clockwiseQuadrantIndices = np.array([[5,4,1,0],\
                                         [6,2,7,3],\
                                         [10,11,14,15],\
                                         [9,13,8,12]], dtype=int)
    counterclockwiseQuadrantIndices = np.array([[5,1,4,0],\
                                         [6,7,2,3],\
                                         [10,14,11,15],\
                                         [9,8,13,12]], dtype=int)

    if indOtherVertex == (indVertex - 1)%4: #clockwise
        return regularPoints[quadIndex,clockwiseQuadrantIndices[indVertex, :]]
    else:
        return regularPoints[quadIndex,counterclockwiseQuadrantIndices[indVertex, :]]




def getABsC(_quad, _edge, _vertex, regularPoints):
    """

    :param:_quad: Quad
    :param:_edge: Edge
    :param:_vertex: Vertex
    :param:regularPoints: numpy.ndarray
    :return: A, B1, B2, C
    :rtype: numpy.ndarray([int, int, int, int])
    """

    assert isinstance(regularPoints, np.ndarray)
    assert isinstance(_quad, Quad)
    assert isinstance(_edge, Edge)
    assert isinstance(_vertex, Vertex)

    vertex_inquad_index = _quad.get_vertices().index(_vertex)

    neighbour_vertex = _edge.get_other_vertex(_vertex)
    other_inquad_index = _quad.get_vertices().index(neighbour_vertex)

    return getABsC_ind(_quad.get_id(), vertex_inquad_index, other_inquad_index, regularPoints)










def dualCont_to_ABC_simpl(quad_objs, vert_objs):
    num_quads = quad_objs.__len__()
    num_verts = len(vert_objs)

    points_per_quad = 16

    As = np.full((num_verts,7,2),-1,dtype=int)
    B1s = np.full((num_verts,7,4),-1,dtype=int)
    B2s = np.full((num_verts,7,4),-1,dtype=int)
    Cs = np.full((num_verts,7,2),-1,dtype=int)

    regularPoints = np.arange(num_quads*points_per_quad, dtype=int).reshape((num_quads, points_per_quad))

    for vertex in vert_objs:
        vert_id = int(vertex.get_id())
        # print "Vert. id: %d, Vert. number: %d" % (vertex.get_id(), vert_id)
        number_of_quads = vertex.number_quads()
        assert number_of_quads > 2, "Found course mesh vertex %d with 2 or less quads, probably manifold" % vert_id
        one_edge = next(iter(vertex.get_edges()))
        one_quad = next(iter(one_edge.get_quads()))

        vertex_inquad_index = one_quad.get_vertices().index(vertex)
        for quadIndex in range(number_of_quads):
            # save the vertex ids on the edges closest to B1 and B2
            B1s[vert_id, quadIndex, 3] = B2s[vert_id, quadIndex, 3] = vert_id
            #first save B2 edge, then switch, then save B1 edge
            B2s[vert_id, quadIndex, 2] = one_edge.get_other_vertex(vertex).get_id()
            one_edge = one_quad.get_other_edge_sharing_vertex(one_edge, vertex)
            B1s[vert_id, quadIndex, 2] = one_edge.get_other_vertex(vertex).get_id()

            #get the ABC IDs of the vertex points
            As[vert_id,quadIndex,0],\
                B1s[vert_id,quadIndex,0],\
                B2s[vert_id,quadIndex,0],\
                Cs[vert_id,quadIndex,0] = getABsC(one_quad,one_edge, vertex, regularPoints)

            #save the quad ID
            As[vert_id,quadIndex,1] =\
                B1s[vert_id,quadIndex,1] =\
                B2s[vert_id,quadIndex,1] =\
                Cs[vert_id,quadIndex,1] = int(one_quad.get_id())

            #shift to next quad
            one_quad = one_quad.get_neighbour_sharing_edge(one_edge)

    return As, B1s, B2s, Cs, regularPoints








