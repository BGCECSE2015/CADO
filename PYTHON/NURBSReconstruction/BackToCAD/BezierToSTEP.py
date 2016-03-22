import csv

import FreeCAD
import Part
import Import

def parse_csv_into_matrix(csv_path, out_type):
    matrix = []
    with open(csv_path) as csvfile:
        idxreader = csv.reader(csvfile, delimiter=',')
        for row in idxreader:
            new_row = []
            for idx in row:
                new_row.append(out_type(idx))
            matrix.append(new_row)

    return matrix


def parse_all_from_folder(folder_path):

    bc_idx = parse_csv_into_matrix(folder_path+'/bicubicPatchIndices.csv',int)
    bq_idx = parse_csv_into_matrix(folder_path+'/biquadraticPatchIndices.csv',int)
    bc_pts = parse_csv_into_matrix(folder_path+'/bicubicPatchPoints.csv',float)
    bq_pts = parse_csv_into_matrix(folder_path+'/biquadraticPatchPoints.csv',float)

    return bq_idx, bq_pts, bc_idx, bc_pts


def get_vertices(patch_ids, vertex_list):
    vertices = []
    for v_id in patch_ids:
        v_id = v_id - 1 # MATLAB indexing -> PYTHON indexing!!!
        vertices.append(vertex_list[v_id])
    return vertices


def generate_bezier_patch(degree, vertices):
    patch = Part.BezierSurface()
    patch.increase(degree,degree)

    for i in range(degree+1):
        for j in range(degree+1):
            k = i+j*(degree+1)
            v = vertices[k]
            control_point = FreeCAD.Vector(v[0],v[1],v[2])
            patch.setPole(i+1,j+1,control_point)
            #Part.show(Part.Vertex(control_point))

    Part.show(patch.toShape())


doc = FreeCAD.newDocument("tmp")
print "Document created"

bq_idx, bq_pts, bc_idx, bc_pts = parse_all_from_folder('./TorusFairBezier')
print "Stuff parsed"

deg = 2
for patch in bq_idx:
    vertices = get_vertices(patch, bq_pts)
    generate_bezier_patch(deg, vertices)

print "biquadratic patches plotted"

deg = 3
patch=bc_idx
for patch in bc_idx:
    vertices = get_vertices(patch, bc_pts)
    generate_bezier_patch(deg, vertices)

print "bicubic patches plotted"

__objs__ = FreeCAD.getDocument("tmp").findObjects()

Import.export(__objs__, "./FairTorus.step")
print ".step exported"
