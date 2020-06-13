#!/bin/bash

rm -rf bin/d*

cd bin

echo "================"
echo "Preparing recipe"
echo "================"
cmake -DCMAKE_CXX_COMPILER=$(which g++) \
      -DCMAKE_CXX_FLAGS="-std=c++17 -Wall -g -O1" -LAH ..

echo "================"
echo "Building..."
echo "================"
make
