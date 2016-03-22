__author__ = 'anna'

import numpy as np

from DooSabin import DooSabin
from PetersScheme.Shape import Shape_DooSabin
from PetersScheme.Vertex  import Vertex_DooSabin


def dooSabin_ABC(verts, faces):

    quads = [None]*faces.shape[0]

    listOfVertices = []
    for i in range(len(verts)):
        listOfVertices.append(Vertex_DooSabin(i, verts[i][0], verts[i][1], verts[i][2]))


    for i in range(faces.shape[0]):
        face_vertices = [listOfVertices[faces[i].astype(int)[j]] for j in range(len(faces[i]))]
        quads[i] = Shape_DooSabin(i, face_vertices)

        for vertex in face_vertices:
            vertex.addNeighbouringFace(quads[i])
    #neighbours_test = quads[4].find_neighbors(quads)
    print "DooSabin 1st refinement"
    [vertices_refined, faces_refined] = DooSabin(listOfVertices, quads, 0.5, 1)
    print "DooSabin 2nd refinement"
    [vertices_refined1, faces_refined1] = DooSabin(vertices_refined, faces_refined, 0.5, 2)

    vertA = -1*np.ones((len(verts), 7, 2))
    vertB1 = -1*np.ones((len(verts), 7, 4))
    vertB2 = -1*np.ones((len(verts), 7, 4))
    nonExtraordinaryPoints = -1*np.ones((len(quads), 16))
    vertC = -1*np.ones((len(verts), 7, 2))

    for i in range(len(quads)):
        nonExtraordinaryPoints[i] = [quads[i].ordered_refined_vertices[j]._id for j in range(16)]

    #necessary arrays
    for i in range(len(listOfVertices)):
        for j in range(len(listOfVertices[i].A)):
            vertA[i][j][0] = listOfVertices[i].A[j][1]._id
            vertA[i][j][1] = listOfVertices[i].A[j][1].parentOrigGrid._id
            vertB1[i][j][0] = listOfVertices[i].B1[j][1]._id
            vertB1[i][j][1] = listOfVertices[i].B1[j][1].parentOrigGrid._id
            vertB1[i][j][2] = listOfVertices[i].B1[j][2][0]._id
            vertB1[i][j][3] = listOfVertices[i].B1[j][2][1]._id
            vertB2[i][j][0] = listOfVertices[i].B2[j][1]._id
            vertB2[i][j][1] = listOfVertices[i].B2[j][1].parentOrigGrid._id
            vertB2[i][j][2] = listOfVertices[i].B2[j][2][0]._id
            vertB2[i][j][3] = listOfVertices[i].B2[j][2][1]._id
            vertC[i][j][0] = listOfVertices[i].C[j][1]._id
            vertC[i][j][1] = listOfVertices[i].C[j][1].parentOrigGrid._id

    return vertA, vertB1, vertB2, vertC, nonExtraordinaryPoints