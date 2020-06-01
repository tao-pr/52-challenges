#!/bin/bash

export FLATBUFFER_SRC_DIR=$HOME/3rd/flatbuffers

rm -rf build/*

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