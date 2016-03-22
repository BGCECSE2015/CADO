/*
 * BodyPartsContainer.hpp
 *
 *  Created on: Oct 27, 2015
 *      Author: friedrich
 */

#ifndef DATAWRAPPERS_BODYPARTSCONTAINER_HPP_
#define DATAWRAPPERS_BODYPARTSCONTAINER_HPP_

#include "VoxelShapesContainer.hpp"

#include <string>
/**
 *
 * Ordering:
 * bodyPartsContainer[0] = Body
 * bodyPartsContainer[1] = Fixture
 * bodyPartsContainer[2] = Load
 * bodyPartsContainer[3] = Active
 * bodyPartsContainer[4] = Passive
 */
class BodyPartsContainer {
public:
	BodyPartsContainer(VoxelShape body);
	virtual ~BodyPartsContainer();

	void pushBackToContainer(const VoxelShapesContainer& voxelShapesContainer);
	void pushBackToPart(const VoxelShape& voxelShape,const std::string part);
	void setToPart(const VoxelShapesContainer& voxelContainerShape,const std::string part);
	void resizePart(const int newSize, const std::string part);
	VoxelShapesContainer& getBodyPartContainer(const std::string part);
	VoxelShape& getFaceIndexOfPart(int index, const std::string part);
	bool isBodyVoxel(const int x, const int y, const int z) const;
	bool isPartVoxel(const int x, const int y, const int z, const std::string part);
private:
	VoxelShape _body;
	std::vector<VoxelShapesContainer> _partsContainer;

	int partStringToIndexMapper(std::string part);
};

#endif /* DATAWRAPPERS_BODYPARTSCONTAINER_HPP_ */
