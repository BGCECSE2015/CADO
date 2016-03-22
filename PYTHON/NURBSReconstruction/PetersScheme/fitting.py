from sortAB1B2VIndices import sortAB1B2VIndices
from scaleAwayParameters import scaleAwayParameters
import scipy.sparse as sp

from createNURBSMatrices import createNURBSMatricesAllraised


from writeMatrices import *
from leastSquares import solve_least_squares_problem
from createFairnessControlMeshCoefs import createFairnessControlMeshCoefs
from createGlobalControlMeshCoefs import createGlobalControlMeshCoefs

def fit_NURBS(As, B1s, B2s, Cs, regularPoints, vertices, quads, fine_vertices, parameters, fairnessWeight):
    print "### Preprocessing ###"
    # Throw away any datapoints which are NaN or outside the parameter range [0,1]
    # since these cause trouble. (+ Scale the resulting ones so that max and min
    # param values are 1 and 0 repspectively in both u and v)

    [parameters, fine_vertices] = scaleAwayParameters(parameters, fine_vertices)
    # [As, B1s, B2s, Cs] = sortAB1B2VIndices(As, B1s, B2s, C) # not needed with new sorting of points
    print "Done."

    print "Calculating coefs."
    coefs = createGlobalControlMeshCoefs(parameters, quads, As, B1s, B2s, Cs, regularPoints)
    print "Done."
    print "Calculating fair coefs."
    fair_coefs = createFairnessControlMeshCoefs(quads, As, B1s, B2s, Cs, regularPoints)
    print "fair_coefs.shape = "+str(fair_coefs.shape)
    print "Done."

    print "Sparsifying..."
    sparse_coefs = sp.csr_matrix(coefs)
    sparse_fair_coefs = sp.csr_matrix(fair_coefs)
    print "Done."

    print "Concatenating matrices...."

    joined_verts = sp.vstack([scipy.array(fine_vertices), scipy.zeros([fair_coefs.shape[0], 3])]).todense()
    joined_coefs = sp.vstack([sparse_coefs, fairnessWeight * sparse_fair_coefs])
    print "Done."

    print "Solving least-squares problem..."
    vertices = solve_least_squares_problem(joined_coefs, joined_verts)
    print "Done."
    #print "Writing files..."
    #write_matrix_to_csv(vertices,'vertices.csv')
    #write_matrix_to_asc(vertices,'vertices.asc')
    #write_matrix_to_asc(fine_vertices,'vertices_fine.asc')
    #print "Done."
    print "Calculating NURBS control points..."

    NURBSMatrix, NURBSIndices = createNURBSMatricesAllraised(quads,As,B1s,B2s,Cs,regularPoints,vertices)
    print "Done."
    return NURBSMatrix, NURBSIndices


