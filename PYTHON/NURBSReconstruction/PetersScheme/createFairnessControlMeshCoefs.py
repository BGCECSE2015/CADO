import numpy as np
import scipy.sparse as ssp

from get3x3ControlPointIndexMask import get3x3ControlPointIndexMask
from getBezierPointCoefs import getBiquadraticPatchCoefs
from createBicubicCoefMatrices import createBicubicCoefMatrices
from getExtraOrdCornerIndexMask import getExtraOrdCornerIndexMask
from getPetersControlPointCoefs import getPetersControlPointCoefs

def one4toone2(i):
    return (i) / 3.0


def whichCornerFun(i, j, whichCornerList):
    return whichCornerList[one4toone2(i)][one4toone2(j)]


def createFairnessControlMeshCoefs(quad_list, AVertexList, B1VertexList, B2VertexList, CVertexList,
                                   quad_control_point_indices):
    """
    takes the list of N quads, the corner points and the connectivity
    information and spits out the fairness coefficients as an
    (N*16*3)x(N*16) matrix.
    """
    N = quad_control_point_indices.shape[0] * quad_control_point_indices.shape[1] * 3
    M = quad_control_point_indices.shape[0] * quad_control_point_indices.shape[1]
    max_size = N*14 #(4x7)x4 for extr. vertices, 12x9 for ordinary, then averaged => 13, one extra for safety (large estimate)
    rows = np.zeros(max_size, dtype=int)
    cols = np.zeros(max_size, dtype=int)
    data = np.zeros(max_size)
    #coefsMatrix = np.zeros((N, M))

    """
    precalculate the coefficients between all the vertex control points and
    the bezier control points for 7 different number of intersecting
    edges as a start
    (number of incoming edges(between 3 an 7 hardcoded), [A,B1,B2,C], [in which quad 1-7], bezier point
    first coord, bezier point second coord)
    """

    ordinaryCoefsRaw = np.zeros((3,3,3,3))
    ACoefsRaw = np.zeros((7, 7, 4, 4))
    B1CoefsRaw = np.zeros((7, 7, 4, 4))
    B2CoefsRaw = np.zeros((7, 7, 4, 4))
    CCoefsRaw = np.zeros((7, 7, 4, 4))

    for num_quads in range(3,8):
        ACoefsRaw[num_quads-1, 0:num_quads, :, :], \
        B1CoefsRaw[num_quads-1, 0:num_quads, :, :], \
        B2CoefsRaw[num_quads-1, 0:num_quads, :, :], \
        CCoefsRaw[num_quads-1, 0:num_quads, :, :] = createBicubicCoefMatrices(num_quads)

    for bezierI in range(3):
        for bezierJ in range(3):
            ordinaryCoefsRaw[:, :, bezierI, bezierJ] = getBiquadraticPatchCoefs(bezierI, bezierJ)

    coefsRawTemp = np.zeros((4, 7, 4, 4))

    uu2mat = np.array([[2.0, 2.0, 2.0], [-4.0, -4.0, -4.0], [2.0, 2.0, 2.0]]) / 3.0
    vv2mat = np.transpose(uu2mat)
    uv2mat = np.array([[1.0, 0.0, -1.0], [0.0, 0.0, 0.0], [-1.0, 0.0, 1.0]])
    uu3mat = np.array(
            [[3.0, 3.0, 3.0, 3.0], [-3.0, -3.0, -3.0, -3.0], [-3.0, -3.0, -3.0, -3.0], [3.0, 3.0, 3.0, 3.0]]) / 4.0
    vv3mat = np.transpose(uu3mat)
    uv3mat = np.array([[1.0, 0.0, 0.0, -1.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [-1.0, 0.0, 0.0, 1.0]])

    biqBezCoefs = np.array([uu2mat, 2.0 * uv2mat, vv2mat])
    bicBezCoefs = np.array([uu3mat, 2.0 * uv3mat, vv3mat])

    whichCornerList = np.array([[0, 3], [1, 2]], dtype=int)

    indexCounter = 0

    p = 0
    print "Main Loop Fairness Coeffs"
    for q in range(quad_list.shape[0]):
        if q%100 == 0:
            print "processing quad %d of %d..." % (q, quad_list.shape[0])
        for j in range(4):
            for i in range(4):
                if (i == 0 or i == 3) and (j == 0 or j == 3):  # bicubic patches
                    whichCorner = whichCornerFun(i, j, whichCornerList)
                    indexMask = getExtraOrdCornerIndexMask(quad_list, AVertexList, B1VertexList, B2VertexList,
                                                           CVertexList, quad_control_point_indices, q, whichCorner)
                    numberOfEdges = indexMask.shape[1]

                    coefsRawTemp[0, 0:numberOfEdges, :, :] = ACoefsRaw[numberOfEdges - 1, 0:numberOfEdges, :, :]
                    coefsRawTemp[1, 0:numberOfEdges, :, :] = B1CoefsRaw[numberOfEdges - 1, 0:numberOfEdges, :, :]
                    coefsRawTemp[2, 0:numberOfEdges, :, :] = B2CoefsRaw[numberOfEdges - 1, 0:numberOfEdges, :, :]
                    coefsRawTemp[3, 0:numberOfEdges, :, :] = CCoefsRaw[numberOfEdges - 1, 0:numberOfEdges, :, :]

                    numberOfEntries = numberOfEdges*4

                    for matType in range(3):
                        bezier_points = np.squeeze(bicBezCoefs[matType, :, :])  # squeeze
                        data[indexCounter:(indexCounter + numberOfEntries)] = getPetersControlPointCoefs(bezier_points,
                                                                      coefsRawTemp[:, 0:numberOfEdges, :, :]).flatten()

                        rows[indexCounter:(indexCounter + numberOfEntries)] = p
                        cols[indexCounter:(indexCounter + numberOfEntries)] = indexMask.flatten()[:]
                        indexCounter += numberOfEntries

                        p += 1



                else:  # biquadratic patches
                    neighbourMask = get3x3ControlPointIndexMask(quad_list=quad_list,
                                                                quad_control_point_indices=quad_control_point_indices,
                                                                quad_index=q,
                                                                localIndexXY=np.array([i, j])).astype(int)  # correct??
                    numberOfEntries = 9

                    for matType in range(3):
                        bezier_points = np.squeeze(biqBezCoefs[matType, :, :])

                        data[indexCounter:(indexCounter + numberOfEntries)] = getPetersControlPointCoefs(bezier_points,
                                                                              ordinaryCoefsRaw).flatten()

                        rows[indexCounter:(indexCounter + numberOfEntries)] = p
                        cols[indexCounter:(indexCounter + numberOfEntries)] = neighbourMask.flatten()[:]
                        p += 1

                        indexCounter += numberOfEntries

    return ssp.coo_matrix((data, (rows, cols)), shape=(N, M))