from get_vertices import get_vertices
from generate_bspline_patch import generate_bspline_patch

import FreeCAD

def get_faces_from_points(nurbs_idx, nurbs_pts):
	knots = [0, 0, 0, 0, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 1, 1, 1, 1]
	degree = 3
	n_nodes = 13

	# holds the faces
	faceHolder = []

	assert (knots.__len__() == n_nodes + degree + 1)

	print "Creating FreeCAD Document..."
	doc = FreeCAD.newDocument("tmp")
	print "FreeCAD Document created."

	print "Plotting patches..."
	patch_id = 0
	for patch in nurbs_idx:
		print "Plotting patch no. " + str(patch_id) + "..."
		vertices = get_vertices(patch, nurbs_pts)
		new_patch = generate_bspline_patch(vertices, n_nodes, degree, knots)
		faceHolder.append(new_patch) # add to the list of Faces the patch converted to Shape
		patch_id += 1
	print "All patches plotted."

	return faceHolder
