import FreeCAD
import Import
import Part

def process_nonchanging_domains(nonchanging_file_name, output_file_name):
	if len(nonchanging_file_name) != 0:

		__objs_original__ = FreeCAD.getDocument("tmp").findObjects()
		len_original =len(__objs_original__)
		print "Loading non-changing component..."
		Import.insert(nonchanging_file_name, "tmp")

		# get objects
		__objs__ = FreeCAD.getDocument("tmp").findObjects()

		# create fusion object
		FreeCAD.getDocument("tmp").addObject("Part::MultiFuse", "FusionTool")

		# add objs to FusionTool
		FreeCAD.getDocument("tmp").FusionTool.Shapes = __objs__[0: len(__objs__)]

		# compute
		FreeCAD.getDocument("tmp").recompute()

		# make one solid
		Part.show(Part.makeSolid(FreeCAD.getDocument("tmp").Objects[-1].Shape))

		# remove all except the last
		__objs__ = FreeCAD.getDocument("tmp").findObjects()
		for i in range(0, len(__objs__) - 1):
			FreeCAD.getDocument("tmp").removeObject(__objs__[i].Name)

		print "Exporting BOOLEANED file..."
		__objs__ = FreeCAD.getDocument("tmp").findObjects()
		Part.export(__objs__, output_file_name+"_BOOLEANED.step")
		print "Output file " + output_file_name+"_BOOLEANED.step" + " exported."

