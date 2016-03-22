import numpy as np
import math
import scipy.io as sio
from bernsteinFramework import *

def getBicubicBezierPointCoefs(localParams, coefs_raw):
    '''

    :param localParams: 2-element vector of parameters (u,v)
    :param coefs_raw: 4x7x4x4 matrix of coefficients (k,l,i,j) from bezier point i,j to Peter's control point type k (0=A,1=B1,2=B2,3=C) on patch locally numbered l
    :return: mx4 matrix of the coefficients on the neighbouring (and central) vertex points to that in the center of the patch, for a point with the local parameters localParams on the patch. The first column is the A coef, the second the B1 coefs, the third the B2 coefs, and the fourth the C coefs.
    '''

    m = coefs_raw.shape[1]
    coefsMatrix = np.zeros((4,m))
    for j in range (4): #possible optimisation: vectorize this loop by hardcoding bernstein for degree 3
        for i in range (4):
            #bernstein degree is ^3
            coefsMatrix[:, :] += coefs_raw[:, :, i, j] * bernstein(i, 3, localParams[0]) * bernstein(j, 3, localParams[1])
    return coefsMatrix