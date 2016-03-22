import numpy as np

def getPetersControlPointCoefs(bezierCoefs,coefs_raw):
    '''

    :param bezierCoefs: Bezier points
    :param coefs_raw: bezier-to-control-point coefficients
    :return: Spits out an nxm matrix of the coefficients on the neighbouring (and central) vertex points to that in the center of the patch, for the bezier points specified in the input and the bezier-to-control-point coefficients in coefs_raw.
    '''

    assert type(bezierCoefs) is np.ndarray
    assert type(coefs_raw) is np.ndarray


    #summing using vectorized code by numpy
    coefs_matrix = np.einsum('klij,ij->kl', coefs_raw, bezierCoefs)

    #equivalent loop-code
    # m=coefs_raw.shape[1]
    # n=coefs_raw.shape[0]
    # coefs_matrix = np.zeros((n,m))

    # for j in range(n):
    #     for i in range (n):
    #         controlPointCoef = bezierCoefs[i,j]
    #         for l in range (m):
    #             for k in range (n):
    #                 coefs_matrix[k,l] += coefs_raw[k,l,i,j]*controlPointCoef

    return coefs_matrix
