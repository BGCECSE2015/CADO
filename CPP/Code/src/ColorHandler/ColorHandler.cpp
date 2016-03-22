/*
 * ColorDetector.cpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#include "ColorHandler.hpp"

#include "../Helper/Helper.hpp"

#include <IGESCAFControl_Reader.hxx>
#include <XCAFApp_Application.hxx>
#include <Handle_XCAFApp_Application.hxx>
#include <XCAFDoc_DocumentTool.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <BRepTools.hxx>

#include <gp_Vec.hxx>
#include <gp_Dir.hxx>
#include <BRepPrimAPI_MakePrism.hxx>
#include <Handle_Geom_Surface.hxx>
#include <GeomLProp_SLProps.hxx>

#include <TopoDS_Compound.hxx>
#include <BRep_Builder.hxx>
#include <BRepBuilderAPI_Sewing.hxx>
#include <TopExp_Explorer.hxx>
#include <BRepBuilderAPI_MakeFace.hxx>
#include <TopAbs_Orientation.hxx>
#include <BRepOffsetAPI_MakeOffsetShape.hxx>
#include <BRepPrimAPI_MakeBox.hxx>

#include <TDF_LabelSequence.hxx>
#include <Handle_TDF_Attribute.hxx>
#include <NCollection_Sequence.hxx>

#include <TopoDS.hxx>
#include <TopoDS_Face.hxx>
#include <TopoDS_Shape.hxx>
#include <TopoDS_Shell.hxx>
#include <TopLoc_Location.hxx>
#include <TopLoc_Datum3D.hxx>

#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>
#include <BRepBuilderAPI_Transform.hxx>
#include <BRepOffsetAPI_MakeThickSolid.hxx>

ColorHandler::ColorHandler() {
    Handle_XCAFApp_Application anApp = XCAFApp_Application::GetApplication();
    anApp->NewDocument("MDTV-XCAF", aDocStep);
    anApp->NewDocument("MDTV-XCAF", aDocIges);
    anApp->NewDocument("MDTV-XCAF", aDocStepActive);

    if(!areDocumentsValid()){
    	std::cout << "ColorHandler::ColorHandler: Documents not valid!!" << std::endl;
    	exit(-1);
    }
}

ColorHandler::~ColorHandler() {
	// TODO Auto-generated destructor stub
}


Handle_TDocStd_Document& ColorHandler::getDocStep(){
	return aDocStep;
}

Handle_TDocStd_Document& ColorHandler::getDocIges(){
	return aDocIges;
}

Handle_TDocStd_Document& ColorHandler::getDocStepActive(){
	return aDocStepActive;
}

void ColorHandler::initializeMembers() {
	buildShapesFromDocs();
}

void ColorHandler::buildShapesFromDocs(){
	buildShapeFromDoc(aDocStep, shapeStep);
	buildShapeFromDoc(aDocIges, shapeIges);
}

void ColorHandler::buildActiveShapeFromDocs(){
	buildShapeFromDoc(aDocStepActive, shapeStepActive);
}

void ColorHandler::buildShapeFromDoc(const Handle_TDocStd_Document& doc, TopoDS_Shape& shape) {
	TDF_LabelSequence aLabel;
	Handle_XCAFDoc_ShapeTool myAssembly = XCAFDoc_DocumentTool::ShapeTool(doc->Main());
	myAssembly->GetShapes(aLabel);
	if (aLabel.Length() == 1) {
		TopoDS_Shape result = myAssembly->GetShape(aLabel.Value(1));
		shape = result;
	} else {
		TopoDS_Compound C;
		BRep_Builder B;
		B.MakeCompound(C);
		for (Standard_Integer i = 1; i < aLabel.Length(); ++i) {
			TopoDS_Shape S = myAssembly->GetShape(aLabel.Value(i));
			B.Add(C, S);
		}
		shape = C;
	}
}

void ColorHandler::getCompleteShape(TopoDS_Shape& topoDSShape) {
	topoDSShape = shapeStep;
}

void ColorHandler::getFixtureShapes(ListOfShape& listOfShapes) {
	Quantity_Color red(1,0,0,Quantity_TOC_RGB);
	std::vector<std::vector<double>> unusedVec;
	getColoredFaces(listOfShapes, unusedVec, red, false);
}

void ColorHandler::getActiveShape(TopoDS_Shape& topoDSShape) {
	topoDSShape = shapeStepActive;
}

void ColorHandler::getLoadShapes(ListOfShape& listOfShapes, std::vector<std::vector<double>>& listOfLoads) {
	Quantity_Color blue(0,0,1,Quantity_TOC_RGB);
	getColoredFaces(listOfShapes, listOfLoads, blue, true);
}

void ColorHandler::getColoredFaces(ListOfShape& listOfShapes, std::vector<std::vector<double>>& listOfLoads, const Quantity_Color wantedColor, const bool isLoadSeeked) {
	std::vector<TopoDS_Face> coloredFacesVector;
	findColoredFaces(wantedColor, coloredFacesVector, listOfLoads, isLoadSeeked);
	buildColoredFaces(coloredFacesVector, listOfShapes);
}

void ColorHandler::findColoredFaces(const Quantity_Color& wantedColor, std::vector<TopoDS_Face>& coloredFacesVector, std::vector<std::vector<double>>& colorVector, const bool isLoadSeeked) {
	XCAFDoc_ColorType ctype = XCAFDoc_ColorGen;
	Handle_XCAFDoc_ColorTool myColors = XCAFDoc_DocumentTool::ColorTool(aDocIges->Main());
	Quantity_Color color;
	TopExp_Explorer exStep(shapeStep, TopAbs_FACE);
	TopExp_Explorer exIges(shapeIges, TopAbs_FACE);
	for (; exStep.More(); exStep.Next()) {
		const TopoDS_Face& faceStep = TopoDS::Face(exStep.Current());
		const TopoDS_Face& faceIges = TopoDS::Face(exIges.Current());
		if (myColors->IsSet(faceIges, ctype)
				|| myColors->IsSet(faceIges, XCAFDoc_ColorSurf)
				|| myColors->IsSet(faceIges, XCAFDoc_ColorCurv))
		{
			myColors->GetColor(faceIges, XCAFDoc_ColorGen, color);
			//If we are not looking for a load, we just compare if the current face faceStep
			//with color "color" has the color "wantedColor"
			//If yes, we push the face in the vector
			if (!isLoadSeeked){
				if (color.Red() == wantedColor.Red()
						&& color.Green() == wantedColor.Green()
						&& color.Blue()  == wantedColor.Blue())
				{
					coloredFacesVector.push_back(faceStep);
					std::cout << "ColorHandler::findColoredFaces: Color found: " << color.Red() << " " << color.Green() << " " << color.Blue() << std::endl;
				}
			}
			//If we are looking for a load, then just store the face if it's color is not white
			//Apply color to force transformation here with color = [0,1) => force = (-0.5,0.5)
			else
			{
			if (color.Red() < 1
				&& color.Green() < 1
				&& color.Blue()  < 1){
					std::vector<double> tempColorVec;
					if (color.Red()==0){
						tempColorVec.push_back(color.Red());
					}else if(color.Red() < 0.5){
						tempColorVec.push_back(-color.Red());
					}else if(color.Red() < 1){
						tempColorVec.push_back(-0.5+color.Red());
					}
					if (color.Green()==0){
						tempColorVec.push_back(color.Green());
					}else if(color.Green() < 0.5){
						tempColorVec.push_back(-color.Green());
					}else if(color.Green() < 1){
						tempColorVec.push_back(-0.5+color.Green());
					}
					if (color.Blue()==0){
						tempColorVec.push_back(color.Blue());
					}else if(color.Blue() < 0.5){
						tempColorVec.push_back(-color.Blue());
					}else if(color.Blue() < 1){
						tempColorVec.push_back(-0.5+color.Blue());
					}
					colorVector.push_back(tempColorVec);
					coloredFacesVector.push_back(faceStep);
				}
//				if (color.Red() < 1
//						&& color.Green() < 1
//						&& color.Blue()  < 1)
//				{
//					std::vector<double> tempColorVec;
//					tempColorVec.push_back(-0.5+color.Red());
//					tempColorVec.push_back(-0.5+color.Green());
//					tempColorVec.push_back(-0.5+color.Blue());
//
//					colorVector.push_back(tempColorVec);
//
//					coloredFacesVector.push_back(faceStep);
//					std::cout << "ColorHandler::findColoredFaces: Force found: " << color.Red() << " " << color.Green() << " " << color.Blue() << std::endl;
//				}
			}
		}
		else
		{
			std::cout << "ColorHandler::findColoredFaces: No Color" << std::endl;
		}
		exIges.Next();
	}
}

void ColorHandler::buildColoredFaces( const std::vector<TopoDS_Face>& coloredFacesVector, ListOfShape& listOfShapes) {
	gp_Vec extrudVec;
	for (size_t i = 0; i < coloredFacesVector.size(); ++i) {
		computeInvertedNormal(coloredFacesVector[i], extrudVec);
		BRepPrimAPI_MakePrism mkPrism(coloredFacesVector[i], extrudVec, Standard_False, Standard_True);
		const TopoDS_Shape &extrudedFace = mkPrism.Shape();
		listOfShapes.append(extrudedFace);
	}
	listOfShapes.setSize(coloredFacesVector.size());
}

void ColorHandler::computeInvertedNormal(const TopoDS_Face& findNormalTo, gp_Vec& normal) {
    Standard_Real umin, umax, vmin, vmax;
    BRepTools::UVBounds(findNormalTo, umin, umax, vmin, vmax);
    std::cout << "ColorHandler::computeInvertedNormal: Umin: " << umin << "Umax: " << umax << "Vmin " << vmin << "Vmax " << vmax << std::endl;
    Handle_Geom_Surface surf = BRep_Tool::Surface(findNormalTo); // create surface
    GeomLProp_SLProps props(surf, umin, vmin, 1, 0.01); // get surface properties
    normal = props.Normal(); // get surface normal
    if(findNormalTo.Orientation() == TopAbs_REVERSED){
    	std::cout << "ColorHandler::computeInvertedNormal: Reversing Normal vector" << std::endl;
    	normal.Reverse(); // check orientation
    }
    normal.Multiply(-1);
    std::cout << "ColorHandler::computeInvertedNormal: InvertedNormalVec: [" << normal.X()<< "," << normal.Y() << ","<< normal.Z() << "]" << std::endl;
}

bool ColorHandler::areDocumentsValid() {
	return XCAFDoc_DocumentTool::IsXCAFDocument(aDocStep) && XCAFDoc_DocumentTool::IsXCAFDocument(aDocIges) ;
}

