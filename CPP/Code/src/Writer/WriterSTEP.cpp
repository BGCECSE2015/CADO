/*
 * WriterSTEP.cpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#include "WriterSTEP.hpp"


#include <STEPControl_StepModelType.hxx>

bool Writer_STEP::write(Voxel_BoolDS& voxelShape) {
	stepWriter.Transfer(sewedShape, STEPControl_AsIs);
	stepWriter.Write("sewed.stp");
}
