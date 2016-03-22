import sys

FREECADPATH = '/usr/lib/freecad/lib'
sys.path.append(FREECADPATH)

import FreeCAD
import Import
import Draft
import Part

def reorient_object(input_file_name, output_file_name, refinement_level):
	__objToExport__ = FreeCAD.getDocument("tmp").findObjects()

	# get the original file
	Import.insert(input_file_name, "tmp")

	# get bounding box
	bB = FreeCAD.getDocument("tmp").Objects[-1].Shape.BoundBox

	# create rotation parameters
	displacement = FreeCAD.Vector(2.0, 0.0, 0.0)
	centerRot = FreeCAD.Vector(bB.XMin, 0.5*(bB.YMin+bB.YMax), bB.ZMin)
	axisRot1 = FreeCAD.Vector(0.0, 0.0, 1.0)
	axisRot2 = FreeCAD.Vector(0.0, 1.0, 0.0)
	angleRot1 = 180.0
	angleRot2 = 90.0

	# import the draft module
	import Draft
	Draft.move(FreeCAD.getDocument("tmp").Objects[0], displacement, copy=False) # perform move
	Draft.rotate(FreeCAD.getDocument("tmp").Objects[0], angleRot1, centerRot,axis=axisRot1,copy=False) # perform first rotation
	Draft.rotate(FreeCAD.getDocument("tmp").Objects[0], angleRot2, centerRot,axis=axisRot2,copy=False) # perform second rotation

	# remove originalGeom
	originalGeom = FreeCAD.getDocument("tmp").Objects[-1].Name
	FreeCAD.getDocument("tmp").removeObject(originalGeom)

	print "Exporting RAW file..."
	Part.export(__objToExport__, output_file_name+".step")
	print "Output file " + output_file_name+".step" + " exported."

