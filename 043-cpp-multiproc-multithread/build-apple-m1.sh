#!/bin/sh

mkdir -p bin
cd bin
LLVM_ROOT=$(brew --prefix llvm) # for cmakelist
cmake -DCMAKE_CXX_COMPILER=$(brew --prefix llvm)/bin/clang++ \
      -DDEFAULT_SYSROOT=$(xcrun --show-sdk-path) \
      -DCMAKE_OSX_ARCHITECTURES='arm64' \
      -DLLVM_TARGETS_TO_BUILD='AArch64' \
      -DLLVM_DEFAULT_TARGET_TRIPLE='aarch64-apple-darwin20.1.0' \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLVM_USE_LINKER=lld \
      -DCMAKE_CXX_FLAGS="-std=c++20 -Wall -g -O1" -LAH ..
make