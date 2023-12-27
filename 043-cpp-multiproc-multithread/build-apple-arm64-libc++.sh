#!/bin/sh

# For cross compilation, we can set DCMAKE_OSX_ARCHITECTURES='arm64;arm7;arm7s' so on

# Run `llvm-config` to get more LLVM configurations

mkdir -p bin
cd bin

export LLVM_LIB_DIR="$(llvm-config --libdir) $(llvm-config --libdir)/c++"
export LLVM_INCLUDE_DIR=$(llvm-config --includedir)/c++/v1
export LLVM_ROOT=$(brew --prefix llvm@16) # for cmakelist

export TBB_LIB_DIR="$(brew --prefix tbb)/lib"
export TBB_INCLUDE_DIR="$(brew --prefix tbb)/include"

cmake -DCMAKE_C_COMPILER=$(brew --prefix llvm@16)/bin/clang \
      -DCMAKE_CXX_COMPILER=$(brew --prefix llvm@16)/bin/clang++ \
      -DCMAKE_OSX_SYSROOT=$(xcrun --show-sdk-path) \
      -DCMAKE_OSX_ARCHIECTURES='arm64' \
      -DDEFAULT_SYSROOT=$(xcrun --show-sdk-path) \
      -DCMAKE_OSX_ARCHITECTURES='arm64' \
      -DLLVM_TARGETS_TO_BUILD='aarch64' \
      -DLLVM_DEFAULT_TARGET_TRIPLE=$(llvm-config --host-target) \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLVM_BUILD_RUNTIME=Off \
      -DLLVM_INCLUDE_TESTS=Off \
      -DCMAKE_CXX_FLAGS="-stdlib=libc++ -Wall -g -O1" ..
make

# NOTE: using `libc++` as standard LLVM Clang++ library

# An alternative is `libstdc++` which uses GNU C++ library