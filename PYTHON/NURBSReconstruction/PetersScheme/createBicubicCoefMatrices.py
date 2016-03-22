from __future__ import division

import numpy as np
import math


def createBicubicCoefMatrices(num_of_quads):
    """
    Returns a dictionary with the biquadractic point coefficients of its
    neighbour vertices for each control point (i,j) = 1..4 on the bicubic patch,
    in the form of four vectors of neighbouring vertex point coefs

    Input:
        @param num_of_quads number of quads
    """

    # nomenclature following that of paper of Eck, Hoppe (Automatic
    # Reconstruction of B-Spline Surfaces of Arbitrary Topological Type), from
    # which the formulae are also collected. (except that indices of the
    # control points are, following matlab custom, shifted one higher ;-)  -> Not anymore! :P)

    Acoefs = np.zeros((num_of_quads, 4, 4))
    B1coefs = np.zeros((num_of_quads, 4, 4))
    B2coefs = np.zeros((num_of_quads, 4, 4))
    Ccoefs = np.zeros((num_of_quads, 4, 4))

    c = math.cos(2 * math.pi / num_of_quads)
    a = c / (1.0 - c)

    B1coefs[0][0][0] = 0.25
    B2coefs[0][0][0] = 0.25
    Ccoefs[0][0][0] = 0.25
    Acoefs[0][0][0] = 0.25

    B1coefs[0][1][0] = 1.0 / 12.0
    B2coefs[0][1][0] = 5.0 / 12.0
    Ccoefs[0][1][0] = 5.0 / 12.0
    Acoefs[0][1][0] = 1.0 / 12.0

    B2coefs[0][2][0] = 5.0 / 12.0
    B1coefs[1][2][0] = 1.0 / 12.0
    Ccoefs[0][2][0] = 5.0 / 12.0
    Ccoefs[1][2][0] = 1.0 / 12.0

    B2coefs[0][3][0] = 0.25
    B1coefs[1][3][0] = 0.25
    Ccoefs[0][3][0] = 0.25
    Ccoefs[1][3][0] = 0.25

    B2coefs[0][1][1] = 5.0 / 36.0
    B1coefs[0][1][1] = 5.0 / 36.0
    Ccoefs[0][1][1] = (25.0 + 4.0 * a) / 36.0
    Acoefs[0][1][1] = (1.0 - 4.0 * a) / 36.0

    B2coefs[0][2][1] = (5.0 - 10.0 * a) / 36.0
    B1coefs[1][2][1] = (1.0 + 2.0 * a) / 36.0
    Ccoefs[0][2][1] = (25.0 + 6.0 * a) / 36.0
    Ccoefs[1][2][1] = (5.0 + 2.0 * a) / 36.0

    for i in range(0, num_of_quads):
        Ccoefs[i][3][3] = 1.0 / num_of_quads

    B2coefs[0][3][1] = (1.0 - 2.0 * a) / 12.0
    B1coefs[1][3][1] = (1.0 - 2.0 * a) / 12.0
    Ccoefs[0][3][1] = (5.0 + 2.0 * a) / 12.0
    Ccoefs[1][3][1] = (5.0 + 2.0 * a) / 12.0

    for i in range(0, num_of_quads):
        Ccoefs[i][3][2] += 1.0 / num_of_quads

    for l in range(0, num_of_quads):
        Ccoefs[l][3][2] += (2.0 * a / (3.0 * c * num_of_quads)) * (np.cos(2.0 * np.pi * (l - 1) / num_of_quads) +
                                                               np.cos(2.0 * np.pi * (l % num_of_quads) / num_of_quads))
    shiftReversed = shiftReverse(0, num_of_quads)

    for j in range(0, 3):
        for i in range(j+1, 4):
            i_symm = j
            j_symm = i

            for k in range(0, num_of_quads):
                Acoefs[k][i_symm][j_symm] = Acoefs[shiftReversed[k]][i][j]
                B1coefs[k][i_symm][j_symm] = B2coefs[shiftReversed[k]][i][j]
                B2coefs[k][i_symm][j_symm] = B1coefs[shiftReversed[k]][i][j]
                Ccoefs[k][i_symm][j_symm] = Ccoefs[shiftReversed[k]][i][j]

    if np.mod(num_of_quads, 2) == 1:
        for i in range(1, num_of_quads+1):
            Ccoefs_h_three_coefs_result = h_three_coefs(i, Ccoefs, c, num_of_quads)
            B1coefs_h_three_coefs_result = h_three_coefs(i, B1coefs, c, num_of_quads)
            B2coefs_h_three_coefs_result = h_three_coefs(i, B2coefs, c, num_of_quads)
            for j in range(0, num_of_quads):
                Ccoefs[j][2][2] -= ((-1) ** i) * Ccoefs_h_three_coefs_result[j]
                B1coefs[j][2][2] -= ((-1) ** i) * B1coefs_h_three_coefs_result[j]
                B2coefs[j][2][2] -= ((-1) ** i) * B2coefs_h_three_coefs_result[j]
    else:
        for i in range(1, num_of_quads+1):
            Ccoefs_h_three_coefs_result = h_three_coefs(i, Ccoefs, c, num_of_quads)
            B1coefs_h_three_coefs_result = h_three_coefs(i, B1coefs, c, num_of_quads)
            B2coefs_h_three_coefs_result = h_three_coefs(i, B2coefs, c, num_of_quads)
            for j in range(0, num_of_quads):
                Ccoefs[j][2][2] -= ((-1) ** i) * (num_of_quads - i) * Ccoefs_h_three_coefs_result[j] * 2.0 / num_of_quads
                B1coefs[j][2][2] -= ((-1) ** i) * (num_of_quads - i) * B1coefs_h_three_coefs_result[j] * 2.0 / num_of_quads
                B2coefs[j][2][2] -= ((-1) ** i) * (num_of_quads - i) * B2coefs_h_three_coefs_result[j] * 2.0 / num_of_quads

    # return {'Acoefs': Acoefs, 'B1coefs': B1coefs, 'B2coefs': B2coefs, 'Ccoefs': Ccoefs}
    return [Acoefs, B1coefs, B2coefs, Ccoefs]


def shiftReverse(ind, modul):
    # Computes a reverse-order index list of length modul-1 starting from index ind
    # Example: shiftReverse(2, 5) returns [2 1 0 4 3]

    shiftReversed = np.mod([ind - i for i in range(0, modul)], modul)
    return shiftReversed


def shifted_indices(ind, modul):
    # Computes a reverse-order index list of length modul-1 starting from index ind
    # Example: shiftReverse(2, 5) returns [2 1 0 4 3]

    shifted = np.mod([ind + i for i in range(0, modul)], modul)
    return shifted


def h_three_coefs(ind, whichArray, c, num_of_quads):
    shiftedIndices = shifted_indices(ind, num_of_quads)
    ans = [0 for i in range(0, len(shiftedIndices))]
    for i in range(0, len(shiftedIndices)):
        ans[i] = (1.0 - 2.0 * c / 3.0) * whichArray[shiftedIndices[i]][3][2] + (2.0 * c / 3.0) * whichArray[
            shiftedIndices[i]][3][1]
    return ans
