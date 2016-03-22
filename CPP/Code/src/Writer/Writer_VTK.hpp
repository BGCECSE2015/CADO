/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef _WRITER_VTK_
#define _WRITER_VTK_

#include "Writer.hpp"

#include <stdlib.h>
#include <iostream>

#include "../Voxelizer/VoxelShape.hpp"
#include <TopoDS_Shape.hxx>
#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>

class Writer_VTK/*: public Writer*/{
public:
    Writer_VTK() /*: Writer() */{}

    ~Writer_VTK() {/*this->~Writer();*/};

    bool write(std::string _filename,  std::vector<std::vector<VoxelShape>> &voxelShape, std::vector<std::vector<double>>& forces);

private:
    void writeHeader(std::ofstream &outfile);

	void writeStructuredGrid(std::ofstream &outfile, VoxelShape &voxelShape);

	void writeScalars(std::ofstream &outfile, VoxelShape &voxelShape);
};

#endif // _WRITER_VTK_
