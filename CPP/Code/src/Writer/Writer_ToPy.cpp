/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#include "Writer_ToPy.hpp"


bool Writer_ToPy::write(std::string _filename, std::vector<std::vector<VoxelShape>> &voxelShape, std::vector<std::vector<double>>& forces, std::string volFraction){
    std::vector<int> dimensions(3);
    dimensions[0]=voxelShape[0][0].getNbX();
    dimensions[1]=voxelShape[0][0].getNbY();
    dimensions[2]=voxelShape[0][0].getNbZ();
    ofstream outfile;
    std::cout << "Writer_ToPy: Writing Tpd file for " + _filename + " .." << std::endl;
    std::cout << "Writer_ToPy: with dimensions: " << dimensions[0] << "," << dimensions[1] << "," << dimensions[2] << std::endl;
    outfile.open(_filename + ".tpd", ios::out | ios::trunc);

    writeHeader(outfile, _filename, volFraction);
    writeDimensions(outfile, dimensions);
    writeGreyScaleFilters(outfile);
	//Write active nodes
	writeNodes("ACTV_ELEM", outfile,voxelShape[3],dimensions);
	//use different voxel shape vector and do the same for the others
	writeNodes("PASV_ELEM",outfile,voxelShape[4],dimensions);
	writeNodes("FXTR_NODE_X",outfile,voxelShape[1],dimensions);
	writeNodes("FXTR_NODE_Y",outfile,voxelShape[1],dimensions);
	writeNodes("FXTR_NODE_Z",outfile,voxelShape[1],dimensions);
	writeNodes("LOAD_NODE_X",outfile,voxelShape[2],dimensions);
	std::vector<int> numberOfLoadVoxelsY = writeNodes("LOAD_NODE_Y",outfile,voxelShape[2],dimensions);
	writeNodes("LOAD_NODE_Z",outfile,voxelShape[2],dimensions);

	//outfile << "LOAD_VALU_Y: " << "-1@" << noLoadVoxelsY << "\n";
	if(numberOfLoadVoxelsY.size()>0){
		writeForces(outfile, forces, numberOfLoadVoxelsY);
	}
    outfile.close();

    std::cout << "Writer_ToPy: .. done!" << std::endl;

    return true;

}

void Writer_ToPy::writeHeader(std::ofstream &outfile, std::string outputName, std::string volFraction){
	outfile << "[ToPy Problem Definition File v2007]\n";
	outfile << "\n";

	outfile << "PROB_TYPE:   comp\n";
	outfile << "PROB_NAME:   " << outputName << "\n";
	outfile << "ETA:         0.4\n";
	outfile << "DOF_PN:      3\n";
	outfile << "VOL_FRAC:    "+volFraction+"\n";
	outfile << "FILT_RAD:    5\n";
	outfile << "ELEM_K:      H8\n";
	outfile << "NUM_ITER:    100\n";
}

void Writer_ToPy::writeDimensions(std::ofstream &outfile, std::vector<int> dimensions){
	outfile << "NUM_ELEM_X:  " << dimensions[0] << "\n";
	outfile << "NUM_ELEM_Y:  " << dimensions[1] << "\n";
	outfile << "NUM_ELEM_Z:  " << dimensions[2] << "\n";
	outfile << "\n";
}

void Writer_ToPy::writeGreyScaleFilters(std::ofstream &outfile){
	outfile << "# Grey-scale filter (GSF)\n";
	outfile << "P_FAC      : 1\n";
	outfile << "P_HOLD     : 15\n";
	outfile << "P_INCR     : 0.2\n";
	outfile << "P_CON      : 1\n";
	outfile << "P_MAX      : 3\n";
	outfile << "\n";
	outfile << "Q_FAC      : 1\n";
	outfile << "Q_HOLD     : 15\n";
	outfile << "Q_INCR     : 0.05\n";
	outfile << "Q_CON      : 1\n";
	outfile << "Q_MAX      : 5\n";
}

std::vector<int> Writer_ToPy::writeNodes(std::string name, std::ofstream &outfile,const std::vector<VoxelShape> &voxelShape, std::vector<int> dimensions){
	std::vector<int> size;
	int originVoxelX = 0;
	int originVoxelY = 0;
	int originVoxelZ = 0;
	double originX = 0;
	double originY = 0;
	double originZ = 0;
	double voxelSizeX = 0;
	double voxelSizeY = 0;
	double voxelSizeZ = 0;
	outfile<< name << ": ";
	const VoxelShape tmpVoxelShape;
	for(size_t h = 0; h < voxelShape.size(); h++){
		originX =voxelShape[h].getOriginX();
		originY =voxelShape[h].getOriginY();
		originZ =voxelShape[h].getOriginZ();
		voxelSizeX = voxelShape[h].getXLen()/voxelShape[h].getNbX();
		voxelSizeY = voxelShape[h].getYLen()/voxelShape[h].getNbY();
		voxelSizeZ = voxelShape[h].getZLen()/voxelShape[h].getNbZ();
		originVoxelX = originX * 1./voxelSizeX;
		originVoxelY = originY * 1./voxelSizeY;
		originVoxelZ = originZ * 1./voxelSizeZ;
		std::cout << "Name: " << name << ": \n"
					 "Origin: "<< "[" << originX << "," << originY << "," << originZ << "] " <<
					 "VoxelOrigin: " << "[" << originVoxelX << "," << originVoxelY <<"," << originVoxelZ<< "] "
					 "VoxelSizes: "<<"[" << voxelSizeX << "," << voxelSizeY <<"," << voxelSizeZ<< "]" << std::endl;
		const std::vector<int>& voxelIndices = voxelShape[h].getIndices();
		for (size_t k = 0; k < voxelIndices.size(); k++){
		//	for (int i = 0; i < voxelShape[h].getVoxelShape().GetNbX(); i++){
		//		for (int j = 0; j < voxelShape[h].getVoxelShape().GetNbY(); j++){
					//std::cout << "Current Step: " << name << ":" << h << "," << k << "," << i << "," << j << std::endl;
		//		if (voxelShape[h].getVoxelShape().Get(i,j,k)==Standard_True){
	//change to list.append
					//std::cout<<"X: "<< i*hx<<" Y:  "<<j*hy<<" Z: "<<k*hz << " Index: "<<(j+(voxelShape[h].getVoxelShape().GetNbY())*(i+k*(voxelShape[h].getVoxelShape().GetNbZ()))) << std::endl;
		//			outfile << (originVoxelY + j+(voxelShape[h].getVoxelShape().GetNbY())*(originVoxelX + i+(originVoxelZ + k)*(voxelShape[h].getVoxelShape().GetNbZ()))) <<"; ";
		//			size++;
		//			}
		//		}
		//	}
		//	if(k < voxelIndices.size()-1)
			if(h == voxelShape.size()-1 && k == voxelIndices.size()-1){
				outfile << voxelIndices[k]+1;
			}else{
				outfile << voxelIndices[k]+1 << "; ";
			}
		}
		size.push_back(voxelIndices.size());
	}
	outfile << "\n";
	return size;
}

void Writer_ToPy::writeForces(std::ofstream &outfile, std::vector<std::vector<double>> &forces, std::vector<int> numberOfLoadVoxels) {
	// Write X loads
	outfile << "LOAD_VALU_X: ";
	for (int i = 0; i < forces.size()-1; i++) {
		outfile << forces[i][0] << "@" << numberOfLoadVoxels[i] << ";";
	}
	outfile << forces.back()[0] << "@" << numberOfLoadVoxels.back() << "\n";

	outfile << "LOAD_VALU_Y: ";
	for (int i = 0; i < forces.size()-1; i++) {
		outfile << forces[i][1] << "@" << numberOfLoadVoxels[i] << ";";
	}
	outfile << forces.back()[1] << "@" << numberOfLoadVoxels.back() << "\n";

	outfile << "LOAD_VALU_Z: ";
	for (int i = 0; i < forces.size()-1; i++) {
		outfile << forces[i][2] << "@" << numberOfLoadVoxels[i] << ";";
	}
	outfile << forces.back()[2] << "@" << numberOfLoadVoxels.back() << "\n";

	outfile << "\n";
}
