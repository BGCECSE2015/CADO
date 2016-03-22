/*
 * VoxelShapesContainer.hpp
 *
 *  Created on: Oct 27, 2015
 *      Author: friedrich
 */

#ifndef DATAWRAPPERS_VOXELSHAPESCONTAINER_HPP_
#define DATAWRAPPERS_VOXELSHAPESCONTAINER_HPP_

#include "../Voxelizer/VoxelShape.hpp"

/*
 *
 */
class VoxelShapesContainer {
public:
	VoxelShapesContainer();
	virtual ~VoxelShapesContainer();

	void pushBack(const VoxelShape& voxelShape);
	VoxelShape& get(const int index);
	int size() const;
	void resize(const unsigned int newSize);

private:
	std::vector<VoxelShape> voxelShapeVector;
};

#endif /* DATAWRAPPERS_VOXELSHAPESCONTAINER_HPP_ */
