/*
 * STEPCAFReader.hpp
 *
 *  Created on: Oct 8, 2015
 *      Author: friedrich
 */

#ifndef READER_STEPCAFREADER_HPP_
#define READER_STEPCAFREADER_HPP_

#include <TopoDS_Shape.hxx>
#include <STEPCAFControl_Reader.hxx>
#include <string>

#include "CAFReader.hpp"
/*
 *
 */
class STEPCAFReader: public CAFReader {
public:
	STEPCAFReader();
	virtual ~STEPCAFReader();

	/**
	 * Reads the file with filename into the stepCAFControlReader
	 * @param filename
	 */
	void read(const std::string filename);

	/**
	 * Transfers the object/model/shape from the reader into the the TDocStd_Document doc
	 * @param doc
	 */
	void transfer(Handle_TDocStd_Document& doc);

private:
	STEPCAFControl_Reader stepCAFControlReader;
};

#endif /* READER_STEPCAFREADER_HPP_ */
