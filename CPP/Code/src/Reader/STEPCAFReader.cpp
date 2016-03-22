/*
 * STEPCAFReader.cpp
 *
 *  Created on: Oct 8, 2015
 *      Author: friedrich
 */

#include "STEPCAFReader.hpp"

#include <Interface_Static.hxx>
#include <Standard_CString.hxx>
#include <TDocStd_Document.hxx>
#include <Handle_TDocStd_Document.hxx>
#include <XCAFApp_Application.hxx>
#include <Handle_XCAFApp_Application.hxx>
#include <XCAFDoc_ShapeTool.hxx>
#include <Handle_XCAFDoc_ShapeTool.hxx>
#include <XCAFDoc_DocumentTool.hxx>
#include <Quantity_Color.hxx>
#include <XCAFDoc_ColorTool.hxx>

STEPCAFReader::STEPCAFReader(): CAFReader() {
}

STEPCAFReader::~STEPCAFReader() {
	this->~CAFReader();
}

void STEPCAFReader::read(const std::string filename) {
	IFSelect_ReturnStatus returnStatus = stepCAFControlReader.ReadFile(filename.c_str());
	switch(returnStatus){
	case IFSelect_RetDone:
		std::cout << "STEPCAFReader::read: File read successful" << std::endl;
		break;
	default:
		std::cout << "STEPCAFReader::read: File read not successful!" << std::endl;
		exit(-1);
	}
	Standard_Integer nbr =  stepCAFControlReader.NbRootsForTransfer();
	std::cout << "STEPCAFReader::read: Number of roots for transfer: " << nbr << std::endl;
}

void STEPCAFReader::transfer(Handle_TDocStd_Document& doc) {
	if(stepCAFControlReader.Transfer(doc)){
		std::cout << "STEPCAFReader::transfer: Transfer successful" << std::endl;
	}else{
		std::cout << "STEPCAFReader::transfer: Transfer failed" << std::endl;
	}
}
