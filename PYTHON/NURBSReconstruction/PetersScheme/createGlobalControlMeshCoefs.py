import numpy as np
import scipy.sparse as ssp

from helper_functions import get_num_edges_meeting
from createBicubicCoefMatrices import createBicubicCoefMatrices
from createLocalParamsExtraordinary import createLocalParamsExtraordinary
from get3x3ControlPointIndexMask import get3x3ControlPointIndexMask
from getBezierPointCoefs import getBezierPointCoefs
from getBicubicBezierPointCoefs import getBicubicBezierPointCoefs
from getExtraOrdCornerIndexMask import getExtraOrdCornerIndexMask


def createGlobalControlMeshCoefs(parameterCoordinates, quad_list, AVertexList, B1VertexList, B2VertexList, CVertexList,
                                     quad_control_point_indices):
    '''
    Takes, for N datapoints, an array parameterCoordinates[Nx3](for every
    datapoint: first entry the quad index, second and third parameters
    on a patch that spans over [0,1]x[0,1]
    for the quad. The function computes the coefficient matrix for between
    each datapoint and the array of M/16 quads x [4x4] vertex control points,
    outputting the coefficients as an N x M scipy.sparse COO-type sparse matrix

    @param parameterCoordinates: Nx3 numpy.ndarray of datapoint parameters
    @param quad_list:
    @param AVertexList:
    @param B1VertexList:
    @param B2VertexList:
    @param CVertexList:
    @param quad_control_point_indices: (M/16)x16 numpy.ndarray of control points on each quad
    @return: NxM scipy.sparse COO-type sparse matrix of coefficients, maximum 22 nonzero entries per row
    '''


    N = parameterCoordinates.shape[0]
    M = quad_control_point_indices.shape[0] * quad_control_point_indices.shape[1]
    max_size = N*28 #4 types of vertices times maximum 7 quads around an extraordinary vertex (large estimate)
    rows = np.zeros(max_size, dtype=int)
    cols = np.zeros(max_size, dtype=int)
    data = np.zeros(max_size)

    """
    Precalculate the coefficients between all the vertex control points and
    the bezier control points for 7 different number of intersecting
    edges as a start

    (number of incoming edges(between 3 an 7 hardcoded), [A,B1,B2,C], [in which quad 1-7], bezier point
    first coord, bezier point second coord)
    """

    ACoefsRaw = np.zeros((7,7,4,4))
    B1CoefsRaw = np.zeros((7,7,4,4))
    B2CoefsRaw = np.zeros((7,7,4,4))
    CCoefsRaw  = np.zeros((7,7,4,4))

    for num_quads in range(3,8):
        [ACoefsRaw[num_quads-1, 0:num_quads, :, :],
         B1CoefsRaw[num_quads-1, 0:num_quads, :, :],
         B2CoefsRaw[num_quads-1, 0:num_quads, :, :],
         CCoefsRaw[num_quads-1, 0:num_quads, :, :]] = createBicubicCoefMatrices(num_quads) # compared to matlab by Saumi & Benni -> VALID

    coefsRawTemp = np.zeros((4,7,4,4))

    indexCounter = 0

    print "Main Loop Coefs"
    for p in range(N):
        if p%100 == 0:
            print "processing point %d of %d..." % (p, N)
        #check if on a corner patch : if both coords are outside [0.25,0.75]
        quadParameters = parameterCoordinates[p, 1:3]
        quad_index = int(parameterCoordinates[p, 0])
        [localCoords, whichCorner, whichPatch] = createLocalParamsExtraordinary(global_quad_params=quadParameters)
        #print "p=%d"%p # todo for p=1 get3x3... fails! -> Resolved(?).
        #print "whichPatch="+str(whichPatch)
        # if there is a specified corner set
        if whichCorner != -1:

            cornerVertexIndex = quad_list[quad_index, whichCorner]

            numberOfEdges = get_num_edges_meeting(AVertexList, cornerVertexIndex)
            #TODO: Check output PROBLEM!
            indexMask = getExtraOrdCornerIndexMask(quad_list, AVertexList, B1VertexList, B2VertexList, CVertexList,
                                                   quad_control_point_indices, quad_index, whichCorner)

            coefsRawTemp[0, 0:numberOfEdges, :, :] = ACoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]
            coefsRawTemp[1, 0:numberOfEdges, :, :] = B1CoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]
            coefsRawTemp[2, 0:numberOfEdges, :, :] = B2CoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]
            coefsRawTemp[3, 0:numberOfEdges, :, :] = CCoefsRaw[numberOfEdges-1, 0:numberOfEdges, :, :]

            patchCoefsMatrix = getBicubicBezierPointCoefs(localCoords, coefsRawTemp[:, 0:numberOfEdges, :, :])

            numberOfEntries = numberOfEdges*4

            rows[indexCounter:(indexCounter + numberOfEntries)] = p
            cols[indexCounter:(indexCounter + numberOfEntries)] = indexMask.flatten()[:]
            data[indexCounter:(indexCounter + numberOfEntries)] = patchCoefsMatrix.flatten()[:]

            indexCounter += numberOfEntries


        else:
            neighbourMask = get3x3ControlPointIndexMask(quad_list=quad_list,
                                                        quad_control_point_indices=quad_control_point_indices,
                                                        quad_index=quad_index,
                                                        localIndexXY=whichPatch)
            neighbourCoefs = getBezierPointCoefs(localCoords)

            numberOfEntries = 9

            rows[indexCounter:(indexCounter + numberOfEntries)] = p
            cols[indexCounter:(indexCounter + numberOfEntries)] = neighbourMask.flatten()[:]
            data[indexCounter:(indexCounter + numberOfEntries)] = neighbourCoefs.flatten()[:]

            indexCounter += numberOfEntries

    print "Main Loop Coeffs Done."

    return ssp.coo_matrix((data, (rows, cols)), shape=(N, M))

