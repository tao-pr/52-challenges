# Have Fun with C++ Multiproc / Multithreading

Playground of C++ features like following

- [Monostate](https://en.cppreference.com/w/cpp/utility/variant/monostate)
- [Bit cast](https://en.cppreference.com/w/cpp/numeric/bit_cast)
- [Range](https://en.cppreference.com/w/cpp/ranges/range)
- [Unordered Map](https://en.cppreference.com/w/cpp/container/unordered_map)
- [Future](https://en.cppreference.com/w/cpp/thread/future)

## Prerequisites

Make sure you have the following in place.

- CMake
- GCC (needs to support C++20)

## Build & Run

Just Cmake it with C++ 20 compiler

```sh
mkdir -p bin
if [ -d bin ]; then
  rm -rf bin/*
fi

cd bin
cmake -DCMAKE_CXX_COMPILER=$(which g++) \
      -DCMAKE_CXX_FLAGS="-std=c++20 -Wall -g -O1" -LAH ..
make
```