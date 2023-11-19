# Have Fun with C++ Multiproc / Multithreading

Playground of C++ features like following. Some are since 11.

- [x] [Monostate](https://en.cppreference.com/w/cpp/utility/variant/monostate)
- [Bit cast](https://en.cppreference.com/w/cpp/numeric/bit_cast)
- [Range](https://en.cppreference.com/w/cpp/ranges/range)
- [Unordered Map](https://en.cppreference.com/w/cpp/container/unordered_map)
- [Constexpr](https://en.cppreference.com/w/cpp/language/constexpr)
- [Future](https://en.cppreference.com/w/cpp/thread/future)
- [Async](https://en.cppreference.com/w/cpp/thread/async)
- [Coroutine](https://en.cppreference.com/w/cpp/language/coroutines)
- [x] [Function Try Block](https://en.cppreference.com/w/cpp/language/function-try-block)
- [Three-way Comparison](https://en.cppreference.com/w/cpp/language/operator_comparison#Three-way_comparison)
- 

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