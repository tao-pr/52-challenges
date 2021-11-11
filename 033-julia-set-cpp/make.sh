#!/bin/bash

export OPENCV_DIR=/usr/local/Cellar/opencv/4.5.0_5/
export OPENCV_INCLUDE_DIR=$OPENCV_DIR/include/opencv4/
export OPENCV_LIB_DIR=$OPENCV_DIR/lib/

# Clean up build dir
# TAOTODO

cd build

echo "================"
echo "Preparing recipe"
echo "================"
cmake -DCMAKE_CXX_COMPILER=$(which g++) \
      -DCMAKE_CXX_FLAGS="-std=c++11 -Wall -g -O1" -LAH ..

echo "================"
echo "Building..."
echo "================"
make
