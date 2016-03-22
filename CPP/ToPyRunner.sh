#!/bin/bash
cd CPP
mkdir -p TopyIO
cd TopyIO
mv ../Code/topy_${1}.tpd .
python ../Code/optimise.py topy_${1}.tpd
cp topy_${1}_099.vtk ../../PYTHON/Extraction/WorkUnstructuredGrid/
cd ../../PYTHON/Extraction/WorkUnstructuredGrid 
python Ugrid_to_Python.py topy_${1}_099.vtk
cd ..
cd ..
cp Extraction/WorkUnstructuredGrid/Cells NURBSReconstruction/
cp Extraction/WorkUnstructuredGrid/Dimensions NURBSReconstruction/


