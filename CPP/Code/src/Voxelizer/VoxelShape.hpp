/*
 * VoxelShape.hpp
 *
 *  Created on: Oct 12, 2015
 *      Author: friedrich
 */

#ifndef VOXELIZER_VOXELSHAPE_HPP_
#define VOXELIZER_VOXELSHAPE_HPP_

#include <Voxel_BoolDS.hxx>
#include <stdlib.h>
#include <vector>
/*
 *
 */
class VoxelShape {
public:
	VoxelShape();
	VoxelShape(Voxel_BoolDS voxelShape);

	~VoxelShape();

	/**
	 * Returns the origin of the voxelShape in the corresponding dimension
	 * @return
	 */
	double getOriginX() const;
	double getOriginY() const;
	double getOriginZ() const;

	/**
	 * Returns the size of the shape in the corresponding dimension
	 * @return
	 */
	double getXLen() const;
	double getYLen() const;
	double getZLen() const;

	/**
	 * Returns the number of voxels in the corresponding dimension
	 * @return
	 */
	int getNbX() const;
	int getNbY() const;
	int getNbZ() const;

	/**
	 * Returns if the cell at (x,y,z) is a voxel
	 * @param x
	 * @param y
	 * @param z
	 * @return
	 */
	bool isVoxel(int x, int y, int z) const;

	/**
	 * Sets the cell at (x,y,z) as isVoxel
	 * @param x
	 * @param y
	 * @param z
	 * @param isVoxel
	 */
	void setVoxel(int x, int y, int z, bool isVoxel);

	Voxel_BoolDS& getVoxelShape();
	Voxel_BoolDS copyVoxelShape();
	void setVoxelShape(const Voxel_BoolDS voxelShape);
	const std::vector<double>& getDimension() const;
	void setDimension(const std::vector<double> dimension);
	std::vector<double> getOrigin() const;

	VoxelShape& operator=( const VoxelShape& other );
	const std::vector<int>& getIndices() const;
	void setIndices(const std::vector<int> indices);
	const std::vector<int> getVoxelDimension() const;
	void setVoxelDimension(const std::vector<int> voxelDimension);

private:
	Voxel_BoolDS _voxelShape;
	std::vector<int> _indices;
	std::vector<double> _dimension;
	std::vector<int> _voxelDimension;
};

#endif /* VOXELIZER_VOXELSHAPE_HPP_ */
