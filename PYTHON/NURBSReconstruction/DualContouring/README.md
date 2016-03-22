# Dual Contouring and Projection
This algorithm performs two resolution DC and then does the projection of fine data onto the coarse mesh. Call
```
verts_coarse, quads_coarse, verts_fine, params = extraction.extract_surface(path)
```
for using our algorithm. The variable ```path``` has to specify a folder with ```Cells``` and ```Dimensions``` (see the folder ```cantilever``` for an example).

This version of DC is copied (antipattern? no way...) from ```BGCEGit/Prototypes/PYTHON/DualContouring/*```