import FreeCAD

def create_mega_bounding_box_object():
	bB0 = FreeCAD.getDocument("tmp").Objects[0].Shape.BoundBox
	bB1 = FreeCAD.getDocument("tmp").Objects[1].Shape.BoundBox

	FreeCAD.ActiveDocument.addObject("Part::Box", "megaBB")
	minX = min(bB0.XMin, bB0.XMin)
	maxX = max(bB0.XMax, bB1.XMax)
	minY = min(bB0.YMin, bB0.YMin)
	maxY = max(bB0.YMax, bB1.YMax)
	minZ = min(bB0.ZMin, bB0.ZMin)
	maxZ = max(bB0.ZMax, bB1.ZMax)

	megaBB_xLen = maxX - minX + 4
	megaBB_yLen = maxY - minY + 4
	megaBB_zLen = maxZ - minZ + 4
	FreeCAD.getDocument("tmp").getObject("megaBB").Length = str(megaBB_xLen)+' mm'
	FreeCAD.getDocument("tmp").getObject("megaBB").Width  = str(megaBB_yLen)+' mm'
	FreeCAD.getDocument("tmp").getObject("megaBB").Height = str(megaBB_zLen)+' mm'
	FreeCAD.getDocument("tmp").getObject("megaBB").Placement = FreeCAD.Placement(FreeCAD.Vector(minX-2, minY-2, minZ-2), FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0), FreeCAD.Vector(0,0,0))
