#!/bin/sh

mkdir -p bin
cd bin
LLVM_ROOT=$(brew --prefix llvm) # for cmakelist
cmake -DCMAKE_C_COMPILER=$(brew --prefix llvm)/bin/clang \
      -DCMAKE_CXX_COMPILER=$(brew --prefix llvm)/bin/clang++ \
      -DCMAKE_OSX_SYSROOT=$(xcrun --show-sdk-path) \
      -DDEFAULT_SYSROOT=$(xcrun --show-sdk-path) \
      -DLDFLAGS=$LDFLAGS \
      -DCMAKE_OSX_ARCHITECTURES='arm64' \
      -DLLVM_TARGETS_TO_BUILD='ARM' \
      -DLLVM_DEFAULT_TARGET_TRIPLE='arm64-apple-darwin23.0.0' \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_CXX_FLAGS="-std=c++17 -Wall -g -O1 -isysroot $(xcrun --show-sdk-path)" ..
make