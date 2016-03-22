/*
 * Voxelizer.cpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#include "Voxelizer.hpp"

#include <iostream>

#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>
#include <Voxel_BoolDS.hxx>
#include <TopTools_ListIteratorOfListOfShape.hxx>
#include "../Helper/Helper.hpp"

void Voxelizer::voxelizeWholeVector(const int refinementLevel, const ListOfShape& listOfShapes, std::vector<VoxelShape>& voxelShapeVector) {
	TopTools_ListIteratorOfListOfShape shapeIterator;
	int counter = 0;
	if(listOfShapes.getSize() > 0){
		for(shapeIterator.Initialize(listOfShapes.getListOfShape()); shapeIterator.More(); shapeIterator.Next() ){
			this->voxelize(shapeIterator.Value(), refinementLevel, voxelShapeVector[counter]);
			counter++;
		}
	}
}

void Voxelizer::voxelize(const TopoDS_Shape topoDSShape,const int refinementLevel, VoxelShape& voxelShape){

    std::cout << "Voxelizer: Getting domain bounds .." << std::endl;

    std::vector<double> origin(3);
    std::vector<double> shapeDimensions(3);
    std::vector<int> voxelDimension(3);
    getBoundingBox(topoDSShape, origin, shapeDimensions);

    for (size_t i = 0; i < 3; i++){
    	voxelDimension[i] = pow(2, refinementLevel) * shapeDimensions[i];
	}

    //Voxel_BoolDS* voxelShapeOCE = new Voxel_BoolDS(); // Result holder of the voxelization
    Standard_Integer progress; // Progress of voxelization (useful in case of parallel code)
    std::cout << "Voxelizer::voxelize: Voxelizing .." << std::endl;
    std::cout << "Voxelizer::voxelize: with number of voxels: " << voxelDimension[0]*voxelDimension[1]*voxelDimension[2] << std::endl;
	Voxel_FastConverter voxelConverter(topoDSShape, voxelShape.getVoxelShape(), 0.1, voxelDimension[0], voxelDimension[1], voxelDimension[2]);
	voxelConverter.FillInVolume(1, topoDSShape);
	voxelConverter.Convert(progress);
	voxelConverter.FillInVolume(1, topoDSShape);
	std::cout << "Voxelizer::voxelize: Progress of Conversion: " << progress << std::endl;
    std::cout << "Voxelizer::voxelize: .. done!" << std::endl;
    voxelShape.setDimension(shapeDimensions);
    voxelShape.setVoxelDimension(voxelDimension);
}

void Voxelizer::getBoundingBox(const TopoDS_Shape topoDSShape, std::vector<double>& origin, std::vector<double>& shapeDimensions){
    Bnd_Box B; // Bounding box
	double Xmin, Ymin, Zmin, Xmax, Ymax, Zmax; // Bounding box bounds
    BRepBndLib::Add(topoDSShape, B);
    B.Get(Xmin, Ymin, Zmin, Xmax, Ymax, Zmax);

    origin[0] = Xmin;
    origin[1] = Ymin;
    origin[2] = Zmin;

    shapeDimensions[0] = absolut(Xmax - Xmin);
    shapeDimensions[1] = absolut(Ymax - Ymin);
    shapeDimensions[2] = absolut(Zmax - Zmin);

    std::cout << "Voxelizer::getBoundingBox:" << std::endl;
    std::cout << "    X[" << Xmin << ", " << Xmax << "]     | xDimension: " << shapeDimensions[0] << std::endl;
    std::cout << "    Y[" << Ymin << ", " << Ymax << "]     | yDimension: " << shapeDimensions[1] << std::endl;
    std::cout << "    Z[" << Zmin << ", " << Zmax << "]     | zDimension: " << shapeDimensions[2] << std::endl;
}

void Voxelizer::fillVolume(VoxelShape& voxelShape){
	//Voxel_BoolDS hollowVoxelShapeDS = voxelShape.getVoxelShape();
	Standard_Real xLen = voxelShape.getXLen();
	Standard_Real yLen = voxelShape.getYLen();
	Standard_Real zLen = voxelShape.getZLen();

	Standard_Real nbX = voxelShape.getNbX();
	Standard_Real nbY = voxelShape.getNbY();
	Standard_Real nbZ = voxelShape.getNbZ();

	std::cout << "Voxelizer::fillVolume: Size: " << xLen << "," << yLen << "," << zLen << std::endl;

	bool inside = false;
	bool prev   = false;
	//Voxel_BoolDS filledVoxelShapeDS = hollowVoxelShapeDS;
	for (Standard_Integer x = 0; x < nbX; x++) {
		for (Standard_Integer y = 0; y < nbY; y++) {
			for (Standard_Integer z = 0; z < nbZ; z++) {

                if (voxelShape.isVoxel(x, y, z)) {
                    if (prev) {
                        inside = true;
                    } else {
                        inside = !inside;
                        //prev = true;
                    }
                } else {
                    if (inside) {
                        voxelShape.setVoxel(x,y,z,Standard_True);
                    } else {
                    }
                }
			}
		}
	}
}

void Voxelizer::getPassiveVoxels(const VoxelShape bodyVoxelShape, VoxelShape& passiveVoxelShape) {
	Standard_Real xLen = bodyVoxelShape.getXLen();
	Standard_Real yLen = bodyVoxelShape.getYLen();
	Standard_Real zLen = bodyVoxelShape.getZLen();

	Standard_Real nbX = bodyVoxelShape.getNbX();
	Standard_Real nbY = bodyVoxelShape.getNbY();
	Standard_Real nbZ = bodyVoxelShape.getNbZ();

	std::cout << "Voxelizer::getPassiveVoxels: Size: " << xLen << "," << yLen << "," << zLen << std::endl;

	//Voxel_BoolDS filledVoxelShapeDS = hollowVoxelShapeDS;
	for (Standard_Integer x = 0; x < nbX; x++) {
		for (Standard_Integer y = 0; y < nbY; y++) {
			for (Standard_Integer z = 0; z < nbZ; z++) {
				/*std::cout << "Voxelizer::getPassiveVoxels: " << x << "," << y <<","<< z <<" Is set: " ;
				std::cout<< bodyVoxelShape.getVoxelShape().Get(x,y,z) << std::endl;
				std::cout << "Read1 done" << std::endl;
				std::cout<< passiveVoxelShape.getVoxelShape().Get(x,y,z) << std::endl;
				std::cout << "Read2 done" << std::endl;*/
				//passiveVoxelShape.getVoxelShape().Set(x,y,z, Standard_True);
				//std::cout << "Set2 done" << std::endl;
				if(bodyVoxelShape.isVoxel(x,y,z)){
					passiveVoxelShape.setVoxel(x,y,z,Standard_False);
				}else{
					passiveVoxelShape.setVoxel(x,y,z,Standard_True);
				}
			}
		}
	}
}
