#Back2CAD

This folder is for all development on the conversion of output data of Peters' scheme (mainly control points and patch distribution) to a standartd CAD format (```.step``` or ```.iges```).

##How to run
We are heavily relying on the **FreeCAD API**. Therefore you first have to install FreeCAD via ```apt-get install freecad```. Then you have to run our script (```NURBSToSTEP```, ```BezierToSTEP``` or ```NURBSToSTEPRaised```) directly from the FreeCAD python interpreter via ```/usr/bin/freecadcmd```.

##Configuration
At the top of the scripts one can configure them (Currently only NURBS script.) by choosing e.g. number of nodes per patch, knot vector...
The following two ```.csv``` files have to be supplied for running the script:

- **All points:** 
    ```NURBSPatchPoints.csv``` a csv file with ```#Pts``` lines and ```3``` columns. Each point (line) is given in cartesian coordinates.
    
    
- **All patches:** 
    ```NURBSPatchPoints.csv``` a csv file with ```#Patches``` lines and ```#Pts per patch``` columns. Each patch (line) is defined by references to the corresponding line in ```NURBSPatchPoints.csv``` (in MATLAB indexing, starting with 1) 

Some valid configurations are given below:

- **All Bezier patches merged into one NURBS patch with minimal number of control points:** Standard config in ```NURBSToSTEP```
    ```python
    knots = [0, 0, 0, 0, 0.25, 0.25, 0.25, 0.5, 0.75, 0.75, 0.75, 1, 1, 1, 1]
    degree = 3
    n_nodes = 11
    ```

- **All Bezier patches merged into one NURBS patch with degree raised to three:*** ```NURBSToSTEPRaised```
    ```python
    knots = [0, 0, 0, 0, .25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 0.75, .75, 1, 1, 1, 1]
    degree = 3
    n_nodes = 13
    ```
    
- **All Control points connected via bilinear patches:**
    ```python
    n_nodes = 11 or 13 or something different    
    knots = [0, 0/n_nodes, 1/n_nodes, ... n_nodes-1/n_nodes, n_nodes/n_nodes, 1]    
    degree = 1    
    ```
