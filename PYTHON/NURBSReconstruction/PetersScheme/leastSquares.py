import numpy as np
import scipy
import scipy.sparse.linalg as lin

def solve_least_squares_problem(A, b):
    x = 3 * [None]
    for i in range(3): # todo scipy does not support least squares with b.shape = (N,3), but only with (N,1) -> Here one computes the QR three times instead of one time! OPTIMIZE!!!
        b_red = np.array(b[:,i])
        print "\n\n### least squares %d out of 3...\n" % (i+1)
        ret = lin.lsmr(A, b_red, show=True)
        print "done."
        x[i] = ret[0]

    x = scipy.array(x).T
    print "x: shape "+str(x.shape)
    print x
    return x