/*
 * VoxelShapesContainer.cpp
 *
 *  Created on: Oct 27, 2015
 *      Author: friedrich
 */

#include "VoxelShapesContainer.hpp"

VoxelShapesContainer::VoxelShapesContainer() {
	// TODO Auto-generated constructor stub

}

VoxelShapesContainer::~VoxelShapesContainer() {
	// TODO Auto-generated destructor stub
}

void VoxelShapesContainer::pushBack(const VoxelShape& voxelShape) {
	voxelShapeVector.push_back(voxelShape);
}

VoxelShape& VoxelShapesContainer::get(const int index){
	return voxelShapeVector[index];
}

int VoxelShapesContainer::size() const {
	return voxelShapeVector.size();
}

void VoxelShapesContainer::resize(const unsigned int newSize) {
	voxelShapeVector.resize(newSize);
}
