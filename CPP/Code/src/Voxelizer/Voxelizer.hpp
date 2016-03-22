/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef _VOXELIZER_
#define _VOXELIZER_

#include <stdlib.h>

#include <TopoDS_Shape.hxx>

#include "VoxelShape.hpp"
#include "VoxelIndexCalculator.hpp"
#include "../DataWrappers/ListOfShape.hpp"

/**
 * class Voxelizer, voxelizes a given TopoDS_Shape with the help of OpenCascade
 */
class Voxelizer {
public:
    Voxelizer() {};

    ~Voxelizer() {};

    /**
     * Calls voxelize() for each shape in ListOfShape and stores it in voxelShapeVector
     * @param refinementLevel
     * @param listOfShapes
     * @param voxelShapeVector
     * @param counter
     */
    void voxelizeWholeVector(const int refinementLevel, const ListOfShape& listOfShapes, std::vector<VoxelShape>& voxelShapeVector);

    /**
     * Voxelizes topoDSShape with given refinementLevel and saves VoxelBoolDS in voxelShape
     * @param topoDSShape
     * @param refinementLevel
     * @param voxelShape
     */
    void voxelize(const TopoDS_Shape topoDSShape,const int refinementLevel, VoxelShape& voxelShape);

    /**
     * Fill Volume of voxelShape, since OpenCascade only voxelizes the outer faces and the inside is empty
     * @param voxelShape
     */
    void fillVolume(VoxelShape& voxelShape);

    /**
     * Calculate passiveVoxels by inverting all values in bodyVoxelShape._voxelShape
     * @param bodyVoxelShape
     * @param passiveVoxelShape
     */
    void getPassiveVoxels(const VoxelShape bodyVoxelShape, VoxelShape& passiveVoxelShape);

private:
    /**
     * Computes BoundingBox for the given topoDSShape and stores quantities of interest in origin and shapeDimensions
     * @param topoDSShape
     * @param origin
     * @param shapeDimensions
     */
    void getBoundingBox(const TopoDS_Shape topoDSShape, std::vector<double>& origin, std::vector<double>& shapeDimensions);
};

#endif // _VOXELIZER_
