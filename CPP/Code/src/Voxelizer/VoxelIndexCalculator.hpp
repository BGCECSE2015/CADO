/*
 * VoxelIndexCalculator.hpp
 *
 *  Created on: Oct 20, 2015
 *      Author: friedrich
 */

#ifndef VOXELIZER_VOXELINDEXCALCULATOR_HPP_
#define VOXELIZER_VOXELINDEXCALCULATOR_HPP_

#include "VoxelShape.hpp"
/**
 *Class responsible for calculating for each voxel a topy voxel index
 **/
class VoxelIndexCalculator {
public:
	VoxelIndexCalculator();
	virtual ~VoxelIndexCalculator();

	/**
	 * Calls calculateIndexForVoxelShape for each VoxelShape in voxelShapeVector
	 * @param voxelShapeVector
	 * @param isElem
	 */
	void calculateIndicesForWholeVector(std::vector<VoxelShape>& voxelShapeVector, const bool isElem);

	/**
	 * Calculates the index for each voxel in voxelShape._voxelShape based on ToPy description and stores it in voxelShape._indices
	 * @param voxelShape
	 * @param isElem
	 */
	void calculateIndexForVoxelShape(VoxelShape& voxelShape, bool isElem);

	/**
	 * Calculates the indices for passive nodes by going over the bodyVoxelShape._voxelShape, adding the index of each voxel which
	 * is 0 (=no voxel) in bodyVoxelShape._voxelShape to passiveVoxelShape._indices
	 * @param bodyVoxelShape
	 * @param passiveVoxelShape
	 */
	void calculatePassiveIndexFromBody(VoxelShape& bodyVoxelShape, VoxelShape& passiveVoxelShape);

	/**
	 * Goes over matrixVoxelShapes and removes indices which are currently in multiple different element types
	 * (i.e. for example if indice is member of load as well as fixture)
	 * @param matrixVoxelShapes
	 */
	void removeDoubleIndices(std::vector<std::vector<VoxelShape>>& matrixVoxelShapes);

	/**
	 * Set dimensions, meaning the dimensions of the whole body which is used as reference point for index calculation
	 * @param dimensions
	 */
	void setDimensions(const std::vector<int> dimensions);

	/**
	 * Set origin, meaning the dimensions of the whole body which is used as reference point for index calculation
	 * @param origin
	 */
	void setOrigin(const std::vector<double> origin);
private:
	std::vector<int> dimensions;
	std::vector<double> origin;
};

#endif /* VOXELIZER_VOXELINDEXCALCULATOR_HPP_ */
