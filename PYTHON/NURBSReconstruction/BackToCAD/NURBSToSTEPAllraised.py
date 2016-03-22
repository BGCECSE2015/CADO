from __future__ import division

import sys

FREECADPATH = '/usr/lib/freecad/lib'
sys.path.append(FREECADPATH)

import FreeCAD
import Part
import Import

from get_faces_from_points import get_faces_from_points
from process_allowed_domains import process_allowed_domains
from process_nonchanging_domains import process_nonchanging_domains
from reorient_object import reorient_object

def export_step(nurbs_idx, nurbs_pts, refinement_level, input_file_name, output_file_name, nonchanging_file_name, allowed_domains_file_name):

	# generate and get faces
	faceHolder = get_faces_from_points(nurbs_idx, nurbs_pts)

	# create shell from face list, create solid from shell
	shellHolder = Part.makeShell(faceHolder)
	solidHolder = Part.makeSolid(shellHolder)
	Part.show(solidHolder)

	# here, the part is brought into the right coordinate system 
	# (something somewhere messes it up, but its too late to get into that mess) Laavaa!
	reorient_object(input_file_name, output_file_name, refinement_level)

	# process allowed domains
	process_allowed_domains(allowed_domains_file_name, output_file_name, refinement_level)

	# process non-changing domains
	process_nonchanging_domains(nonchanging_file_name, output_file_name, refinement_level)

	print "Export done."
