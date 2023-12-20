#!/bin/sh

# For cross compilation, we can set DCMAKE_OSX_ARCHITECTURES='arm64;arm7;arm7s' so on

# Run `llvm-config` to get more LLVM configurations

mkdir -p bin
cd bin
LLVM_LIB_DIR=$(llvm-config --libdir)
LLVM_INCLUDE_DIR=$(llvm-config --includedir)
LLVM_ROOT=$(brew --prefix llvm@16) # for cmakelist
cmake -DCMAKE_C_COMPILER=$(brew --prefix llvm@16)/bin/clang \
      -DCMAKE_CXX_COMPILER=$(brew --prefix llvm@16)/bin/clang++ \
      -DCMAKE_OSX_SYSROOT=$(xcrun --show-sdk-path) \
      -DDEFAULT_SYSROOT=$(xcrun --show-sdk-path) \
      -DCMAKE_OSX_ARCHITECTURES='arm64' \
      -DLLVM_TARGETS_TO_BUILD='aarch64' \
      -DLLVM_DEFAULT_TARGET_TRIPLE=$(llvm-config --host-target) \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLVM_BUILD_RUNTIME=Off \
      -DLLVM_INCLUDE_TESTS=Off \
      -DCMAKE_CXX_FLAGS="-std=c++20 -stdlib=libc++ -Wall -g -O1 -isysroot $(xcrun --show-sdk-path)" ..
make

# To include extra projects, use below
# -DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra;libcxx' \