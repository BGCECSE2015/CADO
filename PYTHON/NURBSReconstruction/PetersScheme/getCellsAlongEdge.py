# ported from MATLAB/Sandbox/GSpline/getCellsAlongEdge.m

import numpy as np

def getCellsAlongEdge(quad_list, control_point_indices, quad_index, vertex1, vertex2, cellNumbers):

    # quad indices oriented:
    # 4---3
    # |   |
    # 1---2

    #assert isinstance(quad_list, np.ndarray), "quad_list not np.ndarray!"
    #assert isinstance(control_point_indices, np.ndarray), "control_point_indices not np.ndarray!"
    #assert isinstance(quad_index, int), "quad_index not int!"
    #assert isinstance(vertex1, int), "vertex1 not int!"
    #assert isinstance(vertex2, int), "vertex2 not int!"
    #assert isinstance(cellNumbers, np.ndarray), "cellNumbers not np.ndarray!"

    local_control_point_indices = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]).transpose()

    dirOne = np.array([0.0, 3.0, 3.0, 0.0])
    dirTwo = np.array([0.0, 0.0, 3.0, 3.0])

    neighbourQuad = quad_list[quad_index, :]

    cellIndices = np.zeros(cellNumbers.shape)
    verOneIndex = np.where(neighbourQuad == vertex1)[0]
    verTwoIndex = np.where(neighbourQuad == vertex2)[0]

    verOneLocal = np.array([dirOne[verOneIndex], dirTwo[verOneIndex]], dtype="int64")
    verTwoLocal = np.array([dirOne[verTwoIndex], dirTwo[verTwoIndex]], dtype="int64")

    directionToGo = ((verTwoLocal - verOneLocal)/3.0).astype(int)
    for i in range(len(cellIndices)):
        cellsLocalIndex = verOneLocal + cellNumbers[i]*directionToGo
        local_control_index = local_control_point_indices[cellsLocalIndex[0],cellsLocalIndex[1]]
        cellIndices[i] = control_point_indices[quad_index,local_control_index]

    return cellIndices