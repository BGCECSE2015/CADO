import FreeCAD
import Part
import Import

PLOT_CONTROL_POINTS = False

def generate_bspline_patch(vertices, n_nodes, degree, knots):
	"""
	Generates a bspine patch from the given vertices. Parameters like degree of the patch, knot vector and number of
	control points are defined above.
	:param vertices: lexicographically numbered control points in a 2D Array of 3 component points
	"""
	n_nodes_u = n_nodes
	n_nodes_v = n_nodes
	degree_u = degree
	degree_v = degree
	knot_u = knots
	knot_v = knots

	patch = Part.BSplineSurface()
	patch.increaseDegree(degree_u, degree_v)

	for i in range(4, len(knot_u)-4):
		patch.insertUKnot(knot_u[i], 1, 0) # todo why is the second argument equal to 1? If anyone could explain = awesome
	for i in range(4, len(knot_v)-4):
		patch.insertVKnot(knot_v[i], 1, 0) # todo why is the second argument equal to 1? If anyone could explain = awesome

	for ii in range(0, n_nodes_u):
		for jj in range(0, n_nodes_v):
			k = ii + jj * n_nodes_u
			v = vertices[k]
			control_point = FreeCAD.Vector(v[0], v[1], v[2])
			patch.setPole(ii + 1, jj + 1, control_point, 1)
			if(PLOT_CONTROL_POINTS):
				Part.show(Part.Vertex(control_point))  # plotting corresponding control points, switched on/off in configuration section

	return patch.toShape()
