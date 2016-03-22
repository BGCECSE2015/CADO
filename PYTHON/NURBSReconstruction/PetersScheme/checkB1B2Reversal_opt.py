# ported from MATLAB/Sandbox/GSpline/checkB1B2Reversal_opt.m
import numpy as np


def checkB1B2Reversal_opt(B1,quad_list,quad_index,vertex_index,regularPoints):

    quadNumberLocal = np.where(B1[vertex_index,:,1] == quad_index)[0][0]
    B1fromList = B1[vertex_index,quadNumberLocal,0]
    thisQuad_cornerVertices = quad_list[quad_index,:]
    whichQuadCorner = np.where(thisQuad_cornerVertices == vertex_index)[0][0]

    localB1s = np.array([2,8,15,9])-1
    localB2s = np.array([5,3,12,14])-1
    shouldBeB1 = regularPoints[quad_index,localB1s[whichQuadCorner]]
    shouldBeB2 = regularPoints[quad_index,localB2s[whichQuadCorner]]


    """
    in peter's scheme, and therefore in the parameters, B1 is the left one if
    looking into the quad corner. Since the quad corners go clockwise, that
    means the relevant quad corner and the one after should be
     shouldBeB1Edge = thisQuad_cornerVertices([whichQuadCorner,mod_index(whichQuadCorner+1,4)]);
     shouldBeB2Edge = thisQuad_cornerVertices([whichQuadCorner,mod_index(whichQuadCorner-1,4)]);
    """

    if B1fromList == shouldBeB1:
        isReversed = False
    elif shouldBeB2 == B1fromList:
        isReversed = True
    else:
        print 'quad_index: '
        print quad_index
        print 'vertex_index'
        print vertex_index
        raise Exception('ERROR! Something wrong with the edges around the quads! Function checkB1B2Reversal')

    return isReversed