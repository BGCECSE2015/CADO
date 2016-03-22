import Part
import Import
import FreeCAD

from create_mega_bounding_box_object import create_mega_bounding_box_object

def process_allowed_domains(allowed_domains_file_name, output_file_name, refinement_level):
	if len(allowed_domains_file_name) != 0:
		print "Checking allowed domains..."
		# take the intersection of allowed domains
		# read in step file for allowed domains
		Import.insert(allowed_domains_file_name, "tmp")
		__objs__ = FreeCAD.getDocument("tmp").findObjects()

		# get bounding box of the allowed domains
		# NOTE: ASSUMING ALLOWED DOMAINS ARE ALL FUSED IN ONE OBJECT.
		#import Draft
		#scaleFactor = 2**refinement_level
		#scaleVector = FreeCAD.Vector(scaleFactor, scaleFactor, scaleFactor)
		#Draft.scale(FreeCAD.getDocument("tmp").Objects[0], scaleVector)#, center=FreeCAD.Vector(1,1,1),copy=False) # perfom scaling

		# create mega BB object
		create_mega_bounding_box_object()

		# cut out allowed domains from mega BB object
		FreeCAD.getDocument("tmp").addObject("Part::Cut", "Cut_megaBB")
		FreeCAD.getDocument("tmp").Cut_megaBB.Base = FreeCAD.getDocument("tmp").Objects[-2]
		FreeCAD.getDocument("tmp").Cut_megaBB.Tool = FreeCAD.getDocument("tmp").Objects[-3]
		FreeCAD.getDocument("tmp").recompute()
		#Part.show(Part.makeSolid(FreeCAD.getDocument("tmp").Objects[-1].Shape))

		# cut out not-allowed parts
		FreeCAD.getDocument("tmp").addObject("Part::Cut", "Cut_allowed")
		FreeCAD.getDocument("tmp").Cut_allowed.Base = FreeCAD.getDocument("tmp").Objects[0]
		FreeCAD.getDocument("tmp").Cut_allowed.Tool = FreeCAD.getDocument("tmp").Objects[-2]
		FreeCAD.getDocument("tmp").recompute()
		Part.show(Part.makeSolid(FreeCAD.getDocument("tmp").Objects[-1].Shape))

		# remove everything except the last cut-object
		__objs__ = FreeCAD.getDocument("tmp").findObjects()
		for i in range(0, len(__objs__) - 1):
			FreeCAD.getDocument("tmp").removeObject(__objs__[i].Name)

		# update __objs__
		__objs__ = FreeCAD.getDocument("tmp").findObjects()

		print __objs__

		if len(__objs__) > 1:
			# create a fuse object and union all "Common"s
			FreeCAD.getDocument("tmp").addObject("Part::MultiFuse", "Fuse")
			FreeCAD.getDocument("tmp").Fuse.Shapes = __objs__[1: len(__objs__)]
			print FreeCAD.getDocument("tmp").Fuse.Shapes
			FreeCAD.getDocument("tmp").recompute()

			# remove "Commons"s
			for i in range(0, len(__objs__)):
				FreeCAD.getDocument("tmp").removeObject(__objs__[i].Name)

		# update __objs__
		__objs__ = FreeCAD.getDocument("tmp").findObjects()

		#print "Exporting ALLOWED file..."
		#__objs__ = FreeCAD.getDocument("tmp").findObjects()
		#Part.export(__objs__, output_file_name+"_ALLOWED.step")
		#print "Output file " + output_file_name+"_ALLOWED.step" + " exported."
