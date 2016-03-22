### How these files work

In these files, the NURBS surface made up by 11x11 bicubic NURBS patches are described.

* they all use the _knot vector_ `[0,0,0,0,0.25,0.25,0.25,0.5,0.5,0.75,0.75,0.75,1,1,1,1]`
* in the "`Points`"-file, all the NURBS- control points are described with one point per line, formatted as `[x-coorinate],[y-coordinate],[z-coordinate]`
* in the "`Indices`"-file, the 11x11 points of a NURBS patch are referred to by their line numbers in the "`Points`"-file. Here, each patch has one row, in which the point indices is seperated by commas. The ordering is a simple listing of the rows/columns after each other (interchangable, since the NURBS surfaces are symmetric under exchange of the indices):

`[(1,1)-index], [(1,2)-index], [(1,3)-index], ... , [(1,11)-index], [(2,1)-index], [(2,2)-index], ... , [(2,11)-index], [(3,1)-index], ...`

CAUTION: All indices are MATLAB-style, that is, the first line is referred to as line 1.
