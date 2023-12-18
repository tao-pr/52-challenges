#!/bin/bash

mkdir -p bin
cd bin
LLVM_ROOT=$(brew --prefix llvm) # for cmakelist
cmake -DCMAKE_CXX_COMPILER=$(brew --prefix llvm)/bin/clang \
      -DCMAKE_CXX_FLAGS="-std=c++20 -stdlib=libc++ -Wall -g -O1" -LAH ..
make