/*
 * STEPReader.hpp
 *
 *  Created on: Oct 6, 2015
 *      Author: saumitra
 */

#ifndef _WRITER_
#define _WRITER_

#include <string>
#include <vector>

#include "../Voxelizer/VoxelShape.hpp"


class Writer{
public:
    Writer() {};

    virtual ~Writer() {};

    virtual bool write(std::string _filename, std::vector<std::vector<VoxelShape>> &voxelShape, std::vector<std::vector<double>>& forces);

    virtual bool write(std::string _filename, std::vector<std::vector<VoxelShape>> &voxelShape, std::vector<std::vector<double>>& forces, std::string volFraction);

protected:
};

#endif // _WRITER_
