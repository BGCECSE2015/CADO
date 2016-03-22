/*
 * BodyPartsContainer.cpp
 *
 *  Created on: Oct 27, 2015
 *      Author: friedrich
 */

#include "BodyPartsContainer.hpp"

#include <iostream>
/**
 *
 * Ordering:
 * body = Body
 * bodyPartsContainer[0] = Fixture
 * bodyPartsContainer[1] = Load
 * bodyPartsContainer[2] = Active
 * bodyPartsContainer[3] = Passive
 */
BodyPartsContainer::BodyPartsContainer(VoxelShape body): _body(body) {
	// TODO Auto-generated constructor stub
	_partsContainer.resize(4);
}

BodyPartsContainer::~BodyPartsContainer() {
	// TODO Auto-generated destructor stub
}

void BodyPartsContainer::pushBackToContainer(const VoxelShapesContainer& voxelShapesContainer) {
	_partsContainer.push_back(voxelShapesContainer);
}

void BodyPartsContainer::pushBackToPart(const VoxelShape& voxelShape, std::string part) {
	_partsContainer[partStringToIndexMapper(part)].pushBack(voxelShape);
}

void BodyPartsContainer::setToPart(const VoxelShapesContainer& voxelShapeContainer, std::string part) {
	_partsContainer[partStringToIndexMapper(part)] = voxelShapeContainer;
}

VoxelShapesContainer& BodyPartsContainer::getBodyPartContainer(std::string part) {
	return _partsContainer[partStringToIndexMapper(part)];
}

VoxelShape& BodyPartsContainer::getFaceIndexOfPart(int index, const std::string part) {
	return _partsContainer[partStringToIndexMapper(part)].get(index);
}

int BodyPartsContainer::partStringToIndexMapper(std::string part) {
	if(part.compare("Fixture")==0){
		return 0;
	}else if(part.compare("Load")==0){
		return 1;
	}else if(part.compare("Active")==0){
		return 2;
	}else if(part.compare("Passive")==0){
		return 3;
	}else{
		std::cout << "BodyPartsContainer::partStringToIndexMapper: Wrong part type!" << std::endl;
		exit(-1);
		return -1;
	}
}

void BodyPartsContainer::resizePart(const int newSize, const std::string part) {
	_partsContainer[partStringToIndexMapper(part)].resize(newSize);
}

bool BodyPartsContainer::isBodyVoxel(const int x, const int y,
		const int z) const {
	return _body.isVoxel(x,y,z);
}

bool BodyPartsContainer::isPartVoxel(const int x, const int y, const int z, const std::string part) {
	return true;
}
