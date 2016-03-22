# ported from MATLAB/Sandbox/GSpline/get3x3ControlPointIndexMask.m
from getCellsAlongEdge import getCellsAlongEdge
from getNeighbourSharedEdge import getNeighbourSharedEdge
import numpy as np

def get3x3ControlPointIndexMask(quad_list, quad_control_point_indices, quad_index, localIndexXY):

    assert type(quad_list) is np.ndarray
    assert type(quad_control_point_indices) is np.ndarray
    assert type(quad_index) is int
    assert type(localIndexXY) is np.ndarray

    indexMask = np.zeros([3,3])

    localX = int(localIndexXY[0])
    localY = int(localIndexXY[1])

    local_control_point_indices = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]).transpose()
    maskMinX = 0
    maskMaxX = 2
    maskMinY = 0
    maskMaxY = 2

    if localX is 0:
        neighbourEdge = quad_list[[quad_index,quad_index],[0,3]]
        neighbourIndex = getNeighbourSharedEdge(quad_list,quad_index,neighbourEdge[0],neighbourEdge[1])
        indexMask[0,:] = getCellsAlongEdge(quad_list=quad_list,
                                           control_point_indices=quad_control_point_indices,
                                           quad_index=neighbourIndex,
                                           vertex1=neighbourEdge[0],
                                           vertex2=neighbourEdge[1],
                                           cellNumbers=np.arange((localY-1), (localY+1)+1))
        maskMinX = 1
    elif localX is 3:
        neighbourEdge = quad_list[[quad_index,quad_index],[1,2]]
        neighbourIndex = getNeighbourSharedEdge(quad_list,quad_index,neighbourEdge[0],neighbourEdge[1])
        indexMask[2,:] = getCellsAlongEdge(quad_list=quad_list,
                                           control_point_indices=quad_control_point_indices,
                                           quad_index=neighbourIndex,
                                           vertex1=neighbourEdge[0],
                                           vertex2=neighbourEdge[1],
                                           cellNumbers=np.arange((localY-1), (localY+1)+1))
        maskMaxX = 1
    elif localY is 0:
        neighbourEdge = quad_list[[quad_index,quad_index],[0,1]]
        neighbourIndex = getNeighbourSharedEdge(quad_list,quad_index,neighbourEdge[0],neighbourEdge[1])
        indexMask[:,0] = getCellsAlongEdge(quad_list=quad_list,
                                           control_point_indices=quad_control_point_indices,
                                           quad_index=neighbourIndex,
                                           vertex1=neighbourEdge[0],
                                           vertex2=neighbourEdge[1],
                                           cellNumbers=np.arange((localX-1), (localX+1)+1))
        maskMinY = 1
    elif localY is 3:
        neighbourEdge = quad_list[[quad_index,quad_index],[3,2]]
        neighbourIndex = getNeighbourSharedEdge(quad_list,quad_index,neighbourEdge[0],neighbourEdge[1])
        indexMask[:,2] = getCellsAlongEdge(quad_list=quad_list,
                                           control_point_indices=quad_control_point_indices,
                                           quad_index=neighbourIndex,
                                           vertex1=neighbourEdge[0],
                                           vertex2=neighbourEdge[1],
                                           cellNumbers=np.arange((localX-1), (localX+1)+1))
        maskMaxY = 1

    for j in range(maskMinY,maskMaxY+1):
        for i in range(maskMinX,maskMaxX+1):
            local_control_point_index = local_control_point_indices[localX-1+i,localY-1+j]
            indexMask[i,j] = quad_control_point_indices[quad_index,local_control_point_index]

    return indexMask