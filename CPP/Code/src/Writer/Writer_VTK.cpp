/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#include "Writer_VTK.hpp"

#include <Voxel_BoolDS.hxx>

bool Writer_VTK::write(std::string filename,  std::vector<std::vector<VoxelShape>> &voxelShape, std::vector<std::vector<double>>& forces){
	std::string outputFilename;
	for(size_t i = 0; i < voxelShape.size()-1; ++i){
		switch(i){
		case 0:
			outputFilename = filename + "_body";
			break;
		case 1:
			outputFilename = filename + "_fixture";
			break;
		case 2:
			outputFilename = filename + "_load";
			break;
		case 3:
			outputFilename = filename + "_active";
			break;
		case 4:
			outputFilename = filename + "_passive";
		}
		for(size_t j = 0; j < voxelShape[i].size(); ++j){
		    ofstream outfile;
		    VoxelShape tmpVoxelShape = voxelShape[i][j];
		    std::cout << "Writer_VTK: Writing VTK file for " + outputFilename << j << " .." << std::endl;
		    outfile.open(outputFilename + std::to_string(j) + ".vtk", ios::out | ios::trunc);

		    writeHeader(outfile);
		    writeStructuredGrid(outfile, tmpVoxelShape);
		    writeScalars(outfile, tmpVoxelShape);

		    outfile.close();
		}
	}

    std::cout << "Writer_VTK: .. done!" << std::endl;

    return true;
}

void Writer_VTK::writeHeader(std::ofstream &outfile) {
    outfile << "# vtk DataFile Version 2.0\n";
	outfile << "BGCE Project 2015-16\n";
	outfile << "ASCII\n";
	outfile << "\n";
}

void Writer_VTK::writeStructuredGrid(std::ofstream &outfile, VoxelShape &voxelShape){
	const Voxel_BoolDS& voxelBoolShape = voxelShape.getVoxelShape();
	outfile << "DATASET STRUCTURED_POINTS\n";
	outfile << "DIMENSIONS  " << (int)voxelBoolShape.GetNbX() << " " << (int)voxelBoolShape.GetNbY() << " " << (int)voxelBoolShape.GetNbZ() << "\n";
	outfile << "ORIGIN " << voxelShape.getOriginX() << " " << voxelShape.getOriginY() << " " << voxelShape.getOriginZ() << "\n";
	outfile << "SPACING " << voxelBoolShape.GetXLen() / voxelBoolShape.GetNbX() << " " << voxelBoolShape.GetYLen() / voxelBoolShape.GetNbY() << " " << voxelBoolShape.GetZLen() / voxelBoolShape.GetNbZ() << "\n";
	outfile << "\n";
}


void Writer_VTK::writeScalars(std::ofstream &outfile, VoxelShape &voxelShape){
	const Voxel_BoolDS& voxelBoolShape = voxelShape.getVoxelShape();
	int totalSize = voxelBoolShape.GetNbX() * voxelBoolShape.GetNbY() * voxelBoolShape.GetNbZ();
	//std::cout << voxelShape.GetNbX() << " " << voxelShape.GetNbY() << " " << voxelShape.GetNbZ() << std::endl;
	outfile << "POINT_DATA " << totalSize << " \n";
	outfile << "SCALARS density int 1 \n";
	outfile << "LOOKUP_TABLE default \n";
	for (int k = 0; k < voxelBoolShape.GetNbZ(); k++){
        for (int j = 0; j < voxelBoolShape.GetNbY(); j++){
            for (int i = 0; i < voxelBoolShape.GetNbX(); i++){
                outfile << (int)(voxelBoolShape.Get(i, j, k)) << "\n";
            }
        }
	}
}
