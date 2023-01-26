#!/bin/bash

export OPENCV_DIR=/usr/local/Cellar/opencv/4.6.0/
export OPENCV_INCLUDE_DIR=$OPENCV_DIR/include/opencv4/
export OPENCV_LIB_DIR=$OPENCV_DIR/lib/

# Clean up build dir
mkdir -p build/
rm -rf build/*

cd build

echo "================"
echo "Preparing recipe"
echo "================"
cmake -DCMAKE_CXX_COMPILER=$(which g++) \
      -DCMAKE_CXX_FLAGS="-std=c++20 -Wall -g -O1" -LAH ..

echo "================"
echo "Building..."
echo "================"
make