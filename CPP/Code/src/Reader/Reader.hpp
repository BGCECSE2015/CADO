/*
 * Reader.hpp
 *
 *  Created on: Oct 20, 2015
 *      Author: Saumitra Joshi
 */

#ifndef READER_READER_HPP_
#define READER_READER_HPP_

#include "IGESCAFReader.hpp"
#include "STEPCAFReader.hpp"
#include "../ColorHandler/ColorHandler.hpp"

/**
 * Abstace Reader class
 */
class Reader {
private:
	std::string sourceFilePath;
	std::string sourceFileName;
	IGESCAFReader readerIges;
	STEPCAFReader readerStep;

public:
	Reader(std::string _sourceFilePath, std::string _sourceFileName):
		sourceFilePath(_sourceFilePath),
		sourceFileName(_sourceFileName) {

	}

	virtual ~Reader();

	void read();

	void transfer(ColorHandler& colorHandler);
};


#endif /* READER_READER_HPP_ */
