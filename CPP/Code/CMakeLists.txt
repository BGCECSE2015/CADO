cmake_minimum_required (VERSION 2.6)
project (CADToVoxel)

#-DCMAKE_BUILD_TYPE=Release / -DCMAKE_BUILD_TYPE=Debug

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -fmessage-length=0 -fopenmp -std=c++11 -D_GNU_SOURCE=1 -D_REENTRANT -Dlinux -D__linux__ -Dx86_64 -D__x86_64__")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -pg -g3 -O0")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -mtune=native -march=native")
set(CMAKE_LD_FLAGS "${CMAKE_LD_FLAGS} -L/usr/local/lib -L/usr/local/lib/oce-0.17-dev")

include_directories(/usr/local/include/oce)
link_directories(/usr/local/lib)

# Build application
add_executable(CADToVoxel
src/CADToVoxel.cpp
src/Reader/Reader.cpp
src/Reader/IGESCAFReader.cpp
src/Reader/STEPCAFReader.cpp
src/Voxelizer/Voxelizer.cpp
src/Voxelizer/VoxelShape.cpp
src/Voxelizer/VoxelIndexCalculator.cpp
src/Writer/Writer_ToPy.cpp
src/Writer/Writer_VTK.cpp
src/ColorHandler/ColorHandler.cpp
src/DataWrappers/ListOfShape.cpp
src/DataWrappers/BodyPartsContainer.cpp
src/DataWrappers/VoxelShapesContainer.cpp)

target_link_libraries(CADToVoxel
TKTopAlgo
TKBRep
TKernel
TKMath
TKVoxel
TKXSBase
TKSTEP
TKIGES
TKXDEIGES
TKXDESTEP
TKXCAF
TKLCAF
TKOffset
TKG3d
TKPrim
TKTopAlgo)

#install(TARGETS CADToVoxel DESTINATION bin)
