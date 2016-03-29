# CADO
CADO- Computer Aided Design Optimization

## Description
CADO is the tool of choice for engineers, designer and whoever likes to apply topology optimization on a CAD model and get a result again in CAD format. Written in C++ and Python, this open source software is highly performant and easily expendable. CADO is straightforward to use and gives the user a one-click tool for his design optimization. In more detail, with CADO, the user only has to select a CAD
input file and set the parameters. By issuing the Run command the tool starts the following pipeline:

1. The given geometry is voxelized
2. Topology Optimization with given parameters is applied
3. Surface Points are computed
4. NURBS surface is extracted
5. Boolean operation is executed for final geometry

The installation and usage of CADO as well as the background theory and implementation details are explained in documentation files in the Doc folder:

- Installation_Guide.pdf
- User_Guide.pdf
- CADO_Integrated_Topology_Optimization.pdf

CADO itself is licensed under the open source BSD license.
