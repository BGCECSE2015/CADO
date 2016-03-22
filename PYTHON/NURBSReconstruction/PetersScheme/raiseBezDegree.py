__author__ = 'erik'


def raiseDeg1D(old_bezier_points):
    # raiseDeg1D Raise the order of the bezier curve by 1.
    #   Provided a dxN - matrix of d-dimensional bezier points, the algorithm outputs a
    #   dx(N+1) matrix of bezier points drawing te exact same curve but with a
    #   degree 1 higher. Tested and works.
    import numpy as np

    assert type(old_bezier_points) is np.ndarray

    dimensions = np.size(old_bezier_points, 1)
    new_degree = np.size(old_bezier_points, 0)

    new_bezier_points = np.zeros([new_degree+1, dimensions])

    inv_degree = 1.0/new_degree

    new_bezier_points[0, :] = old_bezier_points[0, :]

    for i in range(1, new_degree):
        new_bezier_points[i, :] = \
            i * inv_degree * old_bezier_points[i-1, :] + \
            (1-i*inv_degree)*old_bezier_points[i, :]

    new_bezier_points[new_degree, :] = old_bezier_points[new_degree-1, :]

    return new_bezier_points


def raiseDeg2D(old_bezier_points):
    # raiseDeg2D Raise the order of the bezier surface by 1.
    #   Provided a dxMxN - matrix of d-dimensional bezier points, the algorithm outputs a
    #   dx(M+1)x(N+1) matrix of bezier points drawing te exact same surface but with a
    #   degree 1 higher. Tested and works.
    import numpy as np

    assert type(old_bezier_points) is np.ndarray

    dimensions = np.size(old_bezier_points, 2)
    new_degreeU = np.size(old_bezier_points, 0)
    new_degreeV = np.size(old_bezier_points, 1)

    half_raised = np.zeros([new_degreeU+1, new_degreeV, dimensions])
    new_bezier_points = np.zeros([new_degreeU+1, new_degreeV+1, dimensions])

    for j in range(new_degreeV):
        half_raised[:, j, :] = raiseDeg1D(np.squeeze(old_bezier_points[:, j, :]))

    for i in range(new_degreeU+1):
        new_bezier_points[i, :, :] = raiseDeg1D(np.squeeze(half_raised[i, :, :]))

    return new_bezier_points


def raiseDeg2D_from3x3(old_bezier_points):
    # raiseDeg2D Raise the order of the bezier surface by 1.
    #   Provided a dxMxN - matrix of d-dimensional bezier points, the algorithm outputs a
    #   dx(M+1)x(N+1) matrix of bezier points drawing te exact same surface but with a
    #   degree 1 higher. Tested and works.
    import numpy as np

    assert type(old_bezier_points) is np.ndarray

    raisingMatrix = np.array([[1,0,0],[1.0/3.0,2.0/3.0,0],[0,1.0/3.0,2.0/3.0],[0,0,1]])

    new_bezier_points = np.einsum('ik,kld,lj->ijd', raisingMatrix, old_bezier_points, raisingMatrix.T)

    return new_bezier_points