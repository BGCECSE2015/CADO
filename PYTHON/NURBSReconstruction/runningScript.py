import argparse

from BackToCAD.NURBSToSTEPAllraised import export_step
from DooSabin.DualCont_to_ABC import dooSabin_ABC
from DualContouring.extraction import extract_surface
from PetersScheme.fitting import fit_NURBS
from PetersScheme.quadvertGenerator import quad_vert_generator
from DooSabin.DualCont_toABC_simple import dualCont_to_ABC_simpl


parser = argparse.ArgumentParser(description='Includes 7 arguments: '
                                             '1)path to Cells and Dimensions 2)path to the input step file'
                                             '3)path to the output file 4)fairnessWeight 5)coarsening_factor'
                                             '6)path to nonchanging file 7)path to allowed domains file')
parser.add_argument('path', type=str, help='path to Cells and Dimensions')
parser.add_argument('input_file_name', type=str, help='path to the input files--given by the user')
parser.add_argument('output_file_name', type=str, help='path to the output file--given by the user')
parser.add_argument('fairnessWeight', type=float, help='fairnessWeight')
parser.add_argument('coarsening_factor', type=int, help='coarsening_factor')
parser.add_argument('refinement_level', type=int, help='refinement_level')
parser.add_argument('nonchanging_file_name', type=str, help='path to nonchanging file --given by the user')
parser.add_argument('allowed_domains_file_name', type=str, help='path to allowed domains file --given by the user')
args, leftovers = parser.parse_known_args()

## todo JC fix this!
if args.nonchanging_file_name is None:
    nonchanging_file_name = ''
else:
    nonchanging_file_name = args.nonchanging_file_name

## todo JC fix this!
if args.allowed_domains_file_name is None:
    allowed_domains_file_name = ''
else:
    allowed_domains_file_name = args.allowed_domains_file_name

args = parser.parse_args()

#####TESTING PATHS ######
#path="./DualContouring/Cantilever"
#input_file_name = "../../OpenCascade/TestGeometry/ActiveVolumeTest/Cantilever.step"
#output_file_name = "./Cantilever"
#fairnessWeight = 0.5
#coarsening_factor = 2
#nonchanging_file_name = "../../OpenCascade/TestGeometry/ActiveVolumeTest/Cantilever_Fixed.step"
#allowed_domains_file_name = "../../OpenCascade/TestGeometry/ActiveVolumeTest/Cantilever_ToOptimize.step"
#######


print "### Surface Extraction ###"
verts_coarse, quads_coarse, verts_fine, parameters = extract_surface(args.path, args.coarsening_factor)
#verts_coarse, quads_coarse, verts_fine, parameters = extract_surface(path, coarsening_factor)
vertices, quads, fine_vertices, new_vertex_list, edges, quad_list = quad_vert_generator(verts_coarse, quads_coarse, verts_fine, parameters)


print "### DooSabin ###"
#A, B1, B2, C, regularPoints = dooSabin_ABC(vertices, quads)    #discontinued
A, B1, B2, C, regularPoints = dualCont_to_ABC_simpl(quad_list, new_vertex_list)
print "### DooSabin DONE ###"

print "### Peters' Scheme ### "
NURBSMatrix, NURBSIndices = fit_NURBS(A, B1, B2, C, regularPoints, vertices, quads, fine_vertices, parameters, args.fairnessWeight)
#NURBSMatrix, NURBSIndices = fit_NURBS(A, B1, B2, C, regularPoints, vertices, quads, fine_vertices, parameters, fairnessWeight)
print "### Peters' Scheme DONE### "

# TODO: nonchanging_file_name should be a zero string if not provided by the user

print "### Generating Step File ###"
export_step( NURBSIndices, NURBSMatrix, args.refinement_level, args.input_file_name, args.output_file_name, nonchanging_file_name, allowed_domains_file_name)
#export_step( NURBSIndices, NURBSMatrix, input_file_name, output_file_name, nonchanging_file_name, allowed_domains_file_name)
print "### Step File DONE### "

