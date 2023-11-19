# Have Fun with C++ Multiproc / Multithreading

Playground of C++ features like following. Some are since 11.

- [x] [Variant](https://en.cppreference.com/w/cpp/utility/variant), [Monostate](https://en.cppreference.com/w/cpp/utility/variant/monostate)
- [x] [asctime, localtime, time_t](https://en.cppreference.com/w/cpp/chrono/c/time)
- [Bit cast](https://en.cppreference.com/w/cpp/numeric/bit_cast)
- [Range](https://en.cppreference.com/w/cpp/ranges/range)
- [Unordered Map](https://en.cppreference.com/w/cpp/container/unordered_map)
- [Constexpr](https://en.cppreference.com/w/cpp/language/constexpr)
- [x] [Future](https://en.cppreference.com/w/cpp/thread/future)
- [x] [Async](https://en.cppreference.com/w/cpp/thread/async)
- [Coroutine](https://en.cppreference.com/w/cpp/language/coroutines)
- [x] [Function Try Block](https://en.cppreference.com/w/cpp/language/function-try-block)
- [Three-way Comparison](https://en.cppreference.com/w/cpp/language/operator_comparison#Three-way_comparison)
- [x] [Lockguard / Mutex](https://en.cppreference.com/w/cpp/thread/lock_guard)

## Prerequisites

Make sure you have the following in place.

- CMake
- GCC (needs to support C++20)

## Pre-run

Generate sample data files for IO-bound tasks

```sh
# num files
N=10

mkdir -p data
rm -f data/*.txt
for (( i=1; i<=N; i++ ))
do
  # Generate a file with a unique name
  FILENAME="./data/file_$i.txt"

  # Num lines (random)
  MAX=13
  MIN=3
  LINES=$((MIN+RANDOM%(MAX-MIN+1)))

  # Length of line (random)
  MAX=10
  MIN=5
  LENGTH=$((MIN+RANDOM%(MAX-MIN+1)))

  # Generate LINES lines of random text and write them to the file
  for (( j=1; j<=LINES; j++ ))
  do
    RANDOM_STRING=$(openssl rand -base64 $LENGTH | tr -dc 'a-zA-Z0-9' | head -c $LENGTH)
    echo $RANDOM_STRING >> $FILENAME
  done
done
```

## Build & Run

Just Cmake it with C++ 20 compiler

```sh
# Optional, cmake will overwrite the compiled binary anyways
mkdir -p bin
if [ -d bin ]; then
  rm -rf bin/*
fi

cd bin
cmake -DCMAKE_CXX_COMPILER=$(which g++) \
      -DCMAKE_CXX_FLAGS="-std=c++20 -Wall -g -O1" -LAH ..
make
```

Then it is recommended to **run from root dir**.

```sh
./bin/mk43
```

## What does the program do?

The program forks `N` processes which each of them will run the following in parallel.

- Randomly run `M` IO-bounded tasks or CPU-bounded tasks. These tasks are run in multi threading.
- For IO-bounded tasks, it reads all .txt files in the directory (with async future).
- For CPU-bounded tasks, it runs **coroutines**.