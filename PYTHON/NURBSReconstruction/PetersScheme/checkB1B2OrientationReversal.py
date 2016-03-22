# ported from MATLAB/Sandbox/GSpline/checkB1B2OrientationReversal.m

import numpy as np
from helper_functions import get_num_edges_meeting

def checkB1B2OrientationReversal(B1,B2,quad_list,quad_index,vertex_index):
    """
    check if the B1 in the quad to the right lies along the same edge as the
    B2 in the current quad.

    :param B1:
    :param B2:
    :param quad_list:
    :param quad_index:
    :param vertex_index:
    :return: a Bool?
    """
    vertex_index = int(vertex_index)

    numberOfEdges = get_num_edges_meeting(B1, vertex_index)

    quadNumberLocal = np.where(B1[vertex_index,:,1] == quad_index)[0][0]

    B1EdgeFromB1 = np.reshape(B1[vertex_index,quadNumberLocal,2:4],2)
    shouldBeSameAsB1Edge = np.reshape(B2[vertex_index,(quadNumberLocal - 1)%numberOfEdges,2:4], 2)
    isB1IfReversed = np.reshape(B2[vertex_index,(quadNumberLocal + 1)%numberOfEdges,2:4],2)
    B2EdgeFromB2 = np.reshape(B2[vertex_index,quadNumberLocal,2:4],2)
    shouldBeSameAsB2Edge = np.reshape(B1[vertex_index,(quadNumberLocal + 1)%numberOfEdges,2:4],2)
    isB2IfReversed = np.reshape(B1[vertex_index,(quadNumberLocal - 1)%numberOfEdges,2:4],2)

    thisQuad_cornerVertices = quad_list[quad_index,:]
    whichQuadCorner = np.where(thisQuad_cornerVertices == vertex_index)[0][0]

    """
    in peter's scheme, and therefore in the parameters, B1 is the left one if
    looking into the quad corner. Since the quad corners go clockwise, that
    means the relevant quad corner and the one after should be
    """
    shouldBeB1Edge = thisQuad_cornerVertices[[whichQuadCorner,(whichQuadCorner+1)%4]]
    shouldBeB2Edge = thisQuad_cornerVertices[[whichQuadCorner, (whichQuadCorner-1)%4]]

    if len(np.intersect1d(B1EdgeFromB1,shouldBeB1Edge)) == 2 and \
        len(np.intersect1d(B2EdgeFromB2,shouldBeB2Edge)) == 2:

        if len(np.intersect1d(B1EdgeFromB1,shouldBeSameAsB1Edge)) == 2 and \
                   len(np.intersect1d(B2EdgeFromB2,shouldBeSameAsB2Edge)) == 2:
            isNotCounterClockwise = False
        elif len(np.intersect1d(B1EdgeFromB1,isB1IfReversed)) == 2 and \
                len(np.intersect1d(B2EdgeFromB2,isB2IfReversed)) == 2:
            isNotCounterClockwise = True
        else:
            raise Exception('something is seriously wrong because the edges don`t add upp. '
                            'in checkB1B2OrientationReversal')

    elif len(np.intersect1d(B1EdgeFromB1,shouldBeB2Edge)) == 2:
        raise Exception('I didn`t write this function and the other one for you to be lazy '
                        'and not use the other to check for reversed b1b2')
    else:
        print 'quad_index: '
        print quad_index
        print 'vertex_index'
        print vertex_index
        raise Exception('ERROR! Something wrong with the edges around the quads! '
                        'Function checkB1B2OrientationReversal')

    return isNotCounterClockwise
