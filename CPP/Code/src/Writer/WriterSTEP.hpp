/*
 * WriterSTEP.hpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#ifndef WRITER_WRITERSTEP_HPP_
#define WRITER_WRITERSTEP_HPP_

#include "Writer.hpp"

#include <stdlib.h>
#include <iostream>
#include <math.h>

#include <TopoDS_Shape.hxx>
#include <Voxel_BoolDS.hxx>
#include <Voxel_FastConverter.hxx>
#include <Bnd_Box.hxx>
#include <BRepBndLib.hxx>
#include <STEPControl_Writer.hxx>
/*
 *
 */
class Writer_STEP: public Writer {
public:
	Writer_STEP(std::string _filename) : Writer(_filename) {}

    ~Writer_STEP() {this->~Writer();}

    bool write(Voxel_BoolDS &voxelShape);

private:
	STEPControl_Writer stepWriter;
};

#endif /* WRITER_WRITERSTEP_HPP_ */
