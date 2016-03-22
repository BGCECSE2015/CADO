import matplotlib.pyplot as plt
import numpy as np
import scipy.io
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from DooSabin.DooSabin import DooSabin


#from Quad_DooSabin import Quad_DooSabin as Quad
#from Vertex_DooSabin import Vertex_DooSabin as Vertex


def dc_to_peter(vertex_list, quad_list):

    quads = []

    verts = [vertex_list[i].get_coordinates()  for i in range(vertex_list.__len__())]

    for i in range(quad_list.__len__()):
        quads.append([quad_list[i].get_vertices()[j].id for j in range(4)])

    faces = np.array(quads)
    verts = np.array(verts)

    quads = [None]*faces.shape[0]

    listOfVertices = []
    for i in range(len(verts)):
        listOfVertices.append(Vertex(i, verts[i]))

    for i in range(faces.shape[0]):
        face_vertices = [listOfVertices[faces[i].astype(int)[j]] for j in range(len(faces[i]))]
        quads[i] = Quad(i, face_vertices)

        for vertex in face_vertices:
            vertex.addNeighbouringFace(quads[i])
    #neighbours_test = quads[4].find_neighbors(quads)

    [vertices_refined, faces_refined] = DooSabin(listOfVertices, quads, 0.5, 1)
    [vertices_refined1, faces_refined1] = DooSabin(vertices_refined, faces_refined, 0.5, 2)


    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_aspect('equal')
    x = []
    y = []
    z = []
    #print(quads[0].ordered_refined_vertices)
    edge_orientation_check = [0, 1, 2, 3]
    #for vertex in quads[2].ordered_refined_vertices:
    for ind in edge_orientation_check:
                x.append(quads[2].ordered_refined_vertices[ind].coordinates[0])
                y.append(quads[2].ordered_refined_vertices[ind].coordinates[1])
                z.append(quads[2].ordered_refined_vertices[ind].coordinates[2])
    x.append(quads[2].vertices[0].coordinates[0])
    y.append(quads[2].vertices[0].coordinates[1])
    z.append(quads[2].vertices[0].coordinates[2])

    x.append(quads[2].vertices[1].coordinates[0])
    y.append(quads[2].vertices[1].coordinates[1])
    z.append(quads[2].vertices[1].coordinates[2])

    # k = 5
    # x.append(listOfVertices[k].coordinates[0])
    # y.append(listOfVertices[k].coordinates[1])
    # z.append(listOfVertices[k].coordinates[2])
    #
    # x.append(listOfVertices[k].B2[0][1].coordinates[0])
    # y.append(listOfVertices[k].B2[0][1].coordinates[1])
    # z.append(listOfVertices[k].B2[0][1].coordinates[2])
    #
    # x.append(listOfVertices[k].B2[0][2][0].coordinates[0])
    # y.append(listOfVertices[k].B2[0][2][0].coordinates[1])
    # z.append(listOfVertices[k].B2[0][2][0].coordinates[2])
    #
    # x.append(listOfVertices[k].B2[0][2][1].coordinates[0])
    # y.append(listOfVertices[k].B2[0][2][1].coordinates[1])
    # z.append(listOfVertices[k].B2[0][2][1].coordinates[2])



    # for i in range(len(listOfVertices[k].A)):
    #     x.append(listOfVertices[k].A[i][1].coordinates[0])
    #     y.append(listOfVertices[k].A[i][1].coordinates[1])
    #     z.append(listOfVertices[k].A[i][1].coordinates[2])
    #
    #     x.append(listOfVertices[k].B1[i][1].coordinates[0])
    #     y.append(listOfVertices[k].B1[i][1].coordinates[1])
    #     z.append(listOfVertices[k].B1[i][1].coordinates[2])
    #
    #     x.append(listOfVertices[k].B2[i][1].coordinates[0])
    #     y.append(listOfVertices[k].B2[i][1].coordinates[1])
    #     z.append(listOfVertices[k].B2[i][1].coordinates[2])
    #
    #     x.append(listOfVertices[k].C[i][1].coordinates[0])
    #     y.append(listOfVertices[k].C[i][1].coordinates[1])
    #     z.append(listOfVertices[k].C[i][1].coordinates[2])

    ax.scatter(x,y,z, color = 'r')
    #x = []
    #y = []
    #z = []
    for face in faces_refined1:
        #print face.quad_id
       # print(face.ordered_refined_vertices)
        n = len(face.vertices)
        # print(face.vertices)
        x = [face.vertices[i].coordinates[0] for i in range(n)]
        y = [face.vertices[i].coordinates[1] for i in range(n)]
        z = [face.vertices[i].coordinates[2] for i in range(n)]
        vtx = [zip(x,y,z)]
        poly = Poly3DCollection(vtx, alpha = 0.2)
        poly.set_color('b')
        poly.set_edgecolor('k')
        ax.add_collection3d(poly)

    # x = []
    # y = []
    # z = []
    # for vertex in listOfVertices:
    #     for i in range(3):
    #
    #         x.append(vertex.A[i][1].coordinates[0])
    #         y.append(vertex.A[i][1].coordinates[1])
    #         z.append(vertex.A[i][1].coordinates[2])
    # ax.scatter(x,y,z, color = 'r')
    # x = []
    # y = []
    # z = []
    # for vertex in listOfVertices:
    #     for i in range(3):
    #
    #         x.append(vertex.C[i][1].coordinates[0])
    #         y.append(vertex.C[i][1].coordinates[1])
    #         z.append(vertex.C[i][1].coordinates[2])
    #
    # ax.scatter(x,y,z, color = 'b')
    vertices =listOfVertices
    x = []
    y = []
    z = []
    # for j in range(len(vertices)):
    #     for i in range(len(vertices[j].B2)):
    #         x.append(vertices[j].B1[i][1].coordinates[0])
    #         y.append(vertices[j].B1[i][1].coordinates[1])
    #         z.append(vertices[j].B1[i][1].coordinates[2])

    ax.scatter(x,y,z, color = 'r')

    x = []
    y = []
    z = []

    # for j in range(len(vertices)):
    #     for i in range(len(vertices[j].B2)):
    #         #print(vertex.B2)
    #         #if (vertex.B2):
    #          x.append(vertices[j].B2[i][1].coordinates[0])
    #          y.append(vertices[j].B2[i][1].coordinates[1])
    #          z.append(vertices[j].B2[i][1].coordinates[2])
    #         #else:
    #         # print(vertex.coordinates)

    ax.scatter(x,y,z, color = 'g')

    x = []
    y = []
    z = []
    # for j in range(1, len(vertices), 3):
    #    x.append(vertices[j].coordinates[0])
    #    y.append(vertices[j].coordinates[1])
    #    z.append(vertices[j].coordinates[2])
    #
    vertA = -1*np.ones((len(verts), 7, 2))
    vertB1 = -1*np.ones((len(verts), 7, 4))
    vertB2 = -1*np.ones((len(verts), 7, 4))
    nonExtraordinaryPoints = -1*np.ones((len(quads), 16))
    vertC = -1*np.ones((len(verts), 7, 2))

    for i in range(len(quads)):
        nonExtraordinaryPoints[i] = [quads[i].ordered_refined_vertices[j].id for j in range(16)]


    for i in range(len(listOfVertices)):
        for j in range(len(listOfVertices[i].A)):
            vertA[i][j][0] = listOfVertices[i].A[j][1].id
            vertA[i][j][1] = listOfVertices[i].A[j][1].parentOrigGrid.quad_id
            vertB1[i][j][0] = listOfVertices[i].B1[j][1].id
            vertB1[i][j][1] = listOfVertices[i].B1[j][1].parentOrigGrid.quad_id
            vertB1[i][j][2] = listOfVertices[i].B1[j][2][0].id
            vertB1[i][j][3] = listOfVertices[i].B1[j][2][1].id
            vertB2[i][j][0] = listOfVertices[i].B2[j][1].id
            vertB2[i][j][1] = listOfVertices[i].B2[j][1].parentOrigGrid.quad_id
            vertB2[i][j][2] = listOfVertices[i].B2[j][2][0].id
            vertB2[i][j][3] = listOfVertices[i].B2[j][2][1].id
            vertC[i][j][0] = listOfVertices[i].C[j][1].id
            vertC[i][j][1] = listOfVertices[i].C[j][1].parentOrigGrid.quad_id

    # Specify the filename of the .mat file
    #matfile = 'torus_point_data.mat'
    matfile = output_file_name+'.mat'


    # Write the array to the mat file. For this to work, the array must be the value
    # corresponding to a key name of your choice in a dictionary
    scipy.io.savemat(matfile, mdict={'A': vertA, 'B1': vertB1, 'B2' : vertB2, 'C' : vertC, 'regularPoints' : nonExtraordinaryPoints}, oned_as='row')

    # For the above line, I specified the kwarg oned_as since python (2.7 with
    # numpy 1.6.1) throws a FutureWarning.  Here, this isn't really necessary
    # since oned_as is a kwarg for dealing with 1-D arrays.

    # Now load in the data from the .mat that was just saved
    matdata = scipy.io.loadmat(matfile)

    # And just to check if the data is the same:
    assert np.all(vertA == matdata['A'])



    ax.scatter(x,y,z, color = 'b')
    ax.set_xlim3d(-1, 2)
    ax.set_ylim3d(-1, 2)
    ax.set_zlim3d(-1, 2)
    plt.show()

