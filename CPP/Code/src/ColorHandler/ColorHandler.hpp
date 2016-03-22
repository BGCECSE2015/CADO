/*
 * ColorHandler.hpp
 *
 *  Created on: Oct 7, 2015
 *      Author: BGCE
 */

#ifndef COLORHANDLER_COLORHANDLER_HPP_
#define COLORHANDLER_COLORHANDLER_HPP_

#include <TDocStd_Document.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <XCAFDoc_ShapeTool.hxx>
#include <Handle_XCAFDoc_ShapeTool.hxx>
#include <Quantity_Color.hxx>
#include <XCAFDoc_ColorTool.hxx>
#include <TDF_LabelSequence.hxx>
#include <TopoDS_Face.hxx>
#include <gp_Vec.hxx>

#include <vector>

#include "../DataWrappers/ListOfShape.hpp"
/**
 * Class responsible from reading the color from the given input files and building shapes from them
 */
class ColorHandler {
public:
	/**
	 * Constructor. Initializes the doc which stores the color informations
	 */
	ColorHandler();
	virtual ~ColorHandler();

	/**
	 * Returns the Document aDocStep
	 * @return
	 */
	Handle_TDocStd_Document& getDocStep();

	/**
	 * Returns the Document aDocIges
	 * @return
	 */
	Handle_TDocStd_Document& getDocIges();

	/**
	 * Returns the Document aDocStepActive
	 * @return
	 */
	Handle_TDocStd_Document& getDocStepActive();

	/**
	 * Initializes the other members of the class
	 */
	void initializeMembers();

	/**
	 * if we have an active shape
	 */
	void buildActiveShapeFromDocs();

	/**
	 * Calls getColoredFaces with color red
	 * @param listOfShapes holds all shapes with the color red
	 */
	void getFixtureShapes(ListOfShape& listOfShapes);

	/**
	 * Calls getColoredFaces with color blue
	 * @param listOfShapes holds all shapes with the color blue
	 */
	void getActiveShape(TopoDS_Shape& topoDSShape);

	/**
	 * Calls getColoredFaces with color green
	 * @param listOfShapes holds all shapes with the color green
	 */
	void getLoadShapes(ListOfShape& listOfShapes, std::vector<std::vector<double>>& listOfLoads);

	/**
     * Returns the faces of the geometry as a TopoDS_Shape.
     */
	void getCompleteShape(TopoDS_Shape& topoDSShape);

private:
    Handle_TDocStd_Document aDocStep;
    Handle_TDocStd_Document aDocStepActive;
    Handle_TDocStd_Document aDocIges;
    Handle_XCAFDoc_ColorTool myColors;
    TopoDS_Shape shapeStep;
    TopoDS_Shape shapeStepActive;
    TopoDS_Shape shapeIges;

    /**
     * called by initialize members
     */
	void buildShapesFromDocs();

	/**
	 * Build TopoDS_Shape from the information stored in doc
	 * @param doc holds the information about the shape
	 * @param shape is the shape built from the document
	 */
    void buildShapeFromDoc(
    		const Handle_TDocStd_Document& 	doc,
    			  TopoDS_Shape& 			shape
			);

	/**
	 * Assembles the shape with the help of the XCAFDoc_ShapeTool myAssembly and the TDF_LabelSequence aLabel.
	 * Steps then through the faces, if they are colored with wantedColor they are added to the
	 * TopTools_ListOfShape& listOfShapes after being build from the faces.
	 * @param listOfShapes holds all shapes with the color wanted color
	 * @param wantedColor the color for which we are looking on the faces
	 */
	void getColoredFaces(
				  ListOfShape& 						listOfShapes,
				  std::vector<std::vector<double>>& listOfLoads,
			const Quantity_Color					wantedColor,
			const bool								isLoadSeeked
			);

	/**
	 * Computes inverted normal of the face
	 */
    void computeInvertedNormal(
    		const TopoDS_Face& 	findNormalTo,
    			  gp_Vec& 		normal
			);

    /**
     * Checks if member documents are valid
     * @return
     */
	bool areDocumentsValid();

	/**
	 * Finds the faces colored with the color wantedColor by stepping through the faces from shapeStep/shapeIGES and the colors given in aDocIges
	 * Apply color to force transformation here with color = [0,1) => force = (-0.5,0.5) if isLoadSeeked=true
	 * @param wantedColor the color we are looking for
	 * @param coloredFacesVector faces of color wantedColor are stored in here
	 * @param colorVector colorVector is stored in here
	 * @param isLoadSeeked are we seeking the load force
	 */
	void findColoredFaces(
			const Quantity_Color& 					wantedColor,
				  std::vector<TopoDS_Face>& 		coloredFacesVector,
				  std::vector<std::vector<double>>& colorVector,
			const bool 								isLoadSeeked
			);

	/**
	 * Builds 3D cuboids with thickness 1 from faces using OpenCascade BRepPrimAPI_MakePrism
	 * @param coloredFacesVector
	 * @param listOfShapes
	 */
	void buildColoredFaces(
			const std::vector<TopoDS_Face>& coloredFacesVector,
				  ListOfShape& 				listOfShapes
			);
};

#endif /* COLORHANDLER_COLORHANDLER_HPP_ */
