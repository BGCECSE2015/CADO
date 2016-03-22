/*
 * ListOfShape.cpp
 *
 *  Created on: Oct 19, 2015
 *      Author: friedrich
 */

#include "ListOfShape.hpp"

ListOfShape::ListOfShape() {
	// TODO Auto-generated constructor stub

}

const TopTools_ListOfShape& ListOfShape::getListOfShape() const {
	return listOfShape;
}

void ListOfShape::setListOfShape(const TopTools_ListOfShape& listOfShape) {
	this->listOfShape = listOfShape;
}

unsigned int ListOfShape::getSize() const {
	return size;
}

void ListOfShape::setSize(unsigned int size) {
	this->size = size;
}

ListOfShape::~ListOfShape() {
	// TODO Auto-generated destructor stub
}

void ListOfShape::append(const TopoDS_Shape& topoDSShape) {
	listOfShape.Append(topoDSShape);
}
