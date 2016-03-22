/*
 * STEPCAFReader.cpp
 *
 *  Created on: Oct 7, 2015
 *      Author: friedrich
 */

#include "IGESCAFReader.hpp"

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

IGESCAFReader::IGESCAFReader(): CAFReader() {
}

IGESCAFReader::~IGESCAFReader() {
	this->~CAFReader();
}

void IGESCAFReader::read(const std::string filename) {
	IFSelect_ReturnStatus returnStatus = igesCAFControlReader.ReadFile(filename.c_str());
	switch(returnStatus){
	case IFSelect_RetDone:
		std::cout << "IGESReader: File read successful" << std::endl;
		break;
	default:
		std::cout << "IGESReader: File read not succesful!" << std::endl;
		exit(-1);
	}
	Standard_Integer nbr =  igesCAFControlReader.NbRootsForTransfer();
	std::cout << "IGESCAFReader: Number of roots for transfer: " << nbr << std::endl;
}

void IGESCAFReader::transfer(Handle_TDocStd_Document& doc) {
	if(igesCAFControlReader.Transfer(doc)){
		std::cout << "IGESCAFReader::transfer: Transfer successful" << std::endl;
	}else{
		std::cout << "IGESCAFReader::transfer: Transfer failed" << std::endl;
	}
}
