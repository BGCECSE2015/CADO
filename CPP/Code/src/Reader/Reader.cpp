/*
 * Reader.cpp
 *
 *  Created on: Oct 19, 2015
 *      Author: Saumitra Joshi
 */

#include <dirent.h>

#include "Reader.hpp"

Reader::~Reader() {
	// TODO Auto-generated destructor stub
}

void Reader::read() {
	// Check file extension
	int len;
	bool stpFlag = false, igsFlag = false;
	struct dirent *pDirent;
	DIR *pDir;

	pDir = opendir(sourceFilePath.c_str());

	std::cout << "Reader: Reading " << sourceFilePath + sourceFileName + ".step" << std::endl;
	readerStep.read(sourceFilePath + sourceFileName + ".step");

	std::cout << "Reader: Reading " << sourceFilePath + sourceFileName + ".iges" << std::endl;
	readerIges.read(sourceFilePath + sourceFileName + ".iges");

}

void Reader::transfer(ColorHandler& colorHandler) {
	readerStep.transfer(colorHandler.getDocStep());
	readerIges.transfer(colorHandler.getDocIges());
}
