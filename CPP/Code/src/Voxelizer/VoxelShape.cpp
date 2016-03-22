/*
 * VoxelShape.cpp
 *
 *  Created on: Oct 12, 2015
 *      Author: friedrich
 */

#include "VoxelShape.hpp"


VoxelShape::VoxelShape(){};

VoxelShape::VoxelShape(Voxel_BoolDS voxelShape): _voxelShape(voxelShape){
}

VoxelShape::~VoxelShape() {
	// TODO Auto-generated destructor stub
	//_voxelShape.Destroy();
}

Voxel_BoolDS& VoxelShape::getVoxelShape() {
	return _voxelShape;
}

std::vector<double> VoxelShape::getOrigin() const {
	return std::vector<double>{getOriginX(), getOriginY(),getOriginZ()};
}

void VoxelShape::setVoxelShape(const Voxel_BoolDS voxelShape) {
	_voxelShape = voxelShape;
}

const std::vector<double>& VoxelShape::getDimension() const {
	return _dimension;
}

void VoxelShape::setDimension(const std::vector<double> dimension) {
	_dimension = dimension;
}

VoxelShape& VoxelShape::operator=( const VoxelShape& other ) {
	      this->_voxelShape = other._voxelShape;
	      this->_dimension = other._dimension;
	      return *this;
}

const std::vector<int>& VoxelShape::getIndices() const {
	return _indices;
}

void VoxelShape::setIndices(const std::vector<int> indices) {
	_indices = indices;
}

Voxel_BoolDS VoxelShape::copyVoxelShape() {
	return _voxelShape;
}

const std::vector<int> VoxelShape::getVoxelDimension() const {
	return _voxelDimension;
}

void VoxelShape::setVoxelDimension(const std::vector<int> voxelDimension) {
	_voxelDimension = voxelDimension;
}

double VoxelShape::getXLen() const{
	return _voxelShape.GetXLen();
}

double VoxelShape::getOriginX() const{
	return _voxelShape.GetX();
}

double VoxelShape::getOriginY() const{
	return _voxelShape.GetY();
}

double VoxelShape::getOriginZ() const{
	return _voxelShape.GetZ();
}

double VoxelShape::getYLen() const{
	return _voxelShape.GetYLen();
}

double VoxelShape::getZLen() const{
	return _voxelShape.GetZLen();
}

int VoxelShape::getNbX() const{
	return _voxelShape.GetNbX();
}

int VoxelShape::getNbY() const{
	return _voxelShape.GetNbY();
}

int VoxelShape::getNbZ() const{
	return _voxelShape.GetNbZ();
}

bool VoxelShape::isVoxel(int x, int y, int z) const{
	return _voxelShape.Get(x,y,z);
}

void VoxelShape::setVoxel(int x, int y, int z, bool isVoxel) {
	_voxelShape.Set(x, y, z, isVoxel);
}
