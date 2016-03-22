/*
 * ListOfShape.hpp
 *
 *  Created on: Oct 19, 2015
 *      Author: friedrich
 */

#ifndef DATAWRAPPERS_LISTOFSHAPE_HPP_
#define DATAWRAPPERS_LISTOFSHAPE_HPP_

#include <TopTools_ListOfShape.hxx>
/*
 *
 */
class ListOfShape {
private:
	TopTools_ListOfShape listOfShape;
	unsigned int size = 0;

public:
	ListOfShape();
	virtual ~ListOfShape();
	void append(const TopoDS_Shape& topoDSShape);
	const TopTools_ListOfShape& getListOfShape() const;
	void setListOfShape(const TopTools_ListOfShape& listOfShape);
	unsigned int getSize() const;
	void setSize(unsigned int size);
};

#endif /* DATAWRAPPERS_LISTOFSHAPE_HPP_ */
