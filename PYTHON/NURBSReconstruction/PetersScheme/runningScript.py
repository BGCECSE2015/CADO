import scipy.io as sio
import numpy as np
import scipy.sparse as sp

from writeMatrices import *
from leastSquares import solve_least_squares_problem
from createFairnessControlMeshCoefs import createFairnessControlMeshCoefs
from createGlobalControlMeshCoefs import createGlobalControlMeshCoefs
from quadvertGenerator import quad_vert_generator
from sortAB1B2VIndices import sortAB1B2VIndices
from scaleAwayParameters import scaleAwayParameters
from createNURBSMatrices import createNURBSMatricesAllraised

# TODO: INSERT dual contouring CODE!
#vertices, quads, fine_vertices = quad_vert_generator()

# For now we use test data to not run Annas slow code
#dc_to_peter(vertex_list, quad_list)

# TODO: No more csv writing and reading!
print "### Initialization ###"
print "Reading csv input..."
parameters = np.genfromtxt('Data/Cantilever_try/parameters.csv', delimiter=';')
quads = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_quads_coarse.csv', delimiter=';'), dtype=int)
vertices = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_verts_coarse.csv', delimiter=';'))
fine_vertices = np.array(np.genfromtxt('Data/Cantilever_try/cantilever_verts_fine.csv', delimiter=';'))
print "Done"

print "Reading mat input..."
mat_contents = sio.loadmat('Data/Cantilever_try/cantilever.mat')

A = mat_contents["A"]
B1 = mat_contents["B1"]
B2 = mat_contents["B2"]
C = mat_contents["C"]
regularPoints= mat_contents["regularPoints"]
print "Done."


print "### Preprocessing ###"
# Throw away any datapoints which are NaN or outside the parameter range [0,1]
# since these cause trouble. (+ Scale the resulting ones so that max and min
# param values are 1 and 0 repspectively in both u and v)

print "Preprocessing of input data..."
[parameters, fine_vertices] = scaleAwayParameters(parameters, fine_vertices)
[newA, newB1, newB2, newC] = sortAB1B2VIndices(A, B1, B2, C)
print "Done."

print "Calculating coefs."
coefs = createGlobalControlMeshCoefs(parameters, quads, newA, newB1, newB2, newC, regularPoints)
print "Done."
print "Calculating fair coefs."
fair_coefs = createFairnessControlMeshCoefs(quads, newA, newB1, newB2, newC, regularPoints)
print "fair_coefs.shape = "+str(fair_coefs.shape)
print "Done."

print "Sparsify..."
sparse_coefs = sp.csr_matrix(coefs)
sparse_fair_coefs = sp.csr_matrix(fair_coefs)
print "Done."

print "Concatenating matrices."
fairnessWeight = 2.0
joined_verts = sp.vstack([scipy.array(fine_vertices), scipy.zeros([fair_coefs.shape[0], 3])]).todense()
joined_coefs = sp.vstack([sparse_coefs, fairnessWeight * sparse_fair_coefs])
print "Done."

print "Least squares..."
vertices = solve_least_squares_problem(joined_coefs, joined_verts)
print "Done."
write_matrix_to_csv(vertices, 'vertices.csv')
write_matrix_to_asc(vertices, 'vertices.asc')

#plotBezierSurfaceWhole(quads, newA, newB1, newB2, newC, regularPoints, vertices)

#[biqPatchPoints,biqIndices,bicPatchPoints,bicIndices] = createBezierPointMatrices(quads_Torus,newA,newB1,newB2,newC,regularPoints,otherVertices);
#csvwrite('biquadraticPatchPoints.csv',biqPatchPoints);
#csvwrite('biquadraticPatchIndices.csv',biqIndices);
#csvwrite('bicubicPatchPoints.csv',bicPatchPoints);
#csvwrite('bicubicPatchIndices.csv',bicIndices);

NURBSMatrix, NURBSIndices = createNURBSMatricesAllraised(quads, newA, newB1, newB2, newC, regularPoints, vertices)
#csvwrite('NURBSPatchPoints.csv',NURBSMatrix);
#csvwrite('NURBSPatchIndices.csv',NURBSIndices);
write_matrix_to_csv(NURBSMatrix, 'NURBSPatchPoints.csv')
write_matrix_to_asc(NURBSMatrix, 'NURBSPatchPoints.asc')
write_matrix_to_csv(NURBSIndices, 'NURBSPatchIndices.csv')
write_matrix_to_asc(NURBSIndices, 'NURBSPatchIndices.asc')
