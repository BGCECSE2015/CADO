/*
 * STEPCAFReader.hpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#ifndef READER_IGESCAFREADER_HPP_
#define READER_IGESCAFREADER_HPP_

#include <TopoDS_Shape.hxx>
#include <IGESCAFControl_Reader.hxx>
#include <string>

#include "CAFReader.hpp"
/*
 *
 */
class IGESCAFReader:public CAFReader {
public:
	IGESCAFReader();
	virtual ~IGESCAFReader();

	/**
	 * Reads the file with filename into the igesCAFControlReader
	 * @param filename
	 */
	void read(const std::string filename);

	/**
	 * Transfers the object/model/shape from the reader into the the TDocStd_Document doc
	 * @param doc
	 */
	void transfer(Handle_TDocStd_Document& doc);

private:
	IGESCAFControl_Reader igesCAFControlReader;
};

#endif /* READER_IGESCAFREADER_HPP_ */
