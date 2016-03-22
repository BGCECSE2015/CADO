/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef _WRITER_TOPY_
#define _WRITER_TOPY_

#include "Writer.hpp"

#include <stdlib.h>
#include <iostream>
#include <math.h>
#include <vector>

#include <TopoDS_Shape.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>

#include "../DataWrappers/BodyPartsContainer.hpp"
#include "../DataWrappers/VoxelShapesContainer.hpp"

/**
 * Writes ToPy output file .tpd
 */
class Writer_ToPy/*: public Writer*/{
public:
    Writer_ToPy() /*: Writer()*/{};

    ~Writer_ToPy() {/*this->~Writer();*/};

    bool write(std::string _filename, std::vector<std::vector<VoxelShape>> &voxelShape, std::vector<std::vector<double>>& forces, std::string volFraction);

private:
    /**
     * Writes the header based on ToPy documentation
     * @param outfile
     * @param _filename
     * @param volFraction
     */
    void writeHeader(std::ofstream &outfile, std::string _filename, std::string volFraction);

    /**
     * Write some parameters based on ToPy documentations
     * @param outfile
     */
    void writeGreyScaleFilters(std::ofstream &outfile);

    /**
     * Write dimensions into the .tdp file
     * @param outfile
     * @param dimensions
     */
    void writeDimensions(std::ofstream &outfile,std::vector<int> dimensions);

    /**
     * Writes the nodes, i.e. active elements, fixtures, loads, passive nodes based on the indices previously calculated
     * and stored in voxelShape
     * @param name
     * @param outfile
     * @param voxelShape
     * @param dimensions
     * @return
     */
    std::vector<int> writeNodes(std::string name, std::ofstream &outfile,const std::vector<VoxelShape> &voxelShape, std::vector<int> dimensions); //later change to vector of shapes

    /**
     * Write the force which is applied on the loads
     * @param outfile
     * @param forces
     * @param numberOfLoadVoxels
     */
    void writeForces(std::ofstream &outfile, std::vector<std::vector<double>> &forces, std::vector<int> numberOfLoadVoxels);
};
#endif // _WRITER_TOPY_
