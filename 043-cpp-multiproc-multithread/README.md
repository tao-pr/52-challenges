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
- [x] [Function Try Block](https://en.cppreference.com/w/cpp/language/function-try-block)
- [Three-way Comparison](https://en.cppreference.com/w/cpp/language/operator_comparison#Three-way_comparison)
- [x] [Lockguard / Mutex](https://en.cppreference.com/w/cpp/thread/lock_guard)

## Prerequisites

Make sure you have the following in place.

- CMake
- [LLVM Compiler](https://github.com/llvm/llvm-project/tree/main) (So it supports `std::execution` which is not available in normal g++/gcc on MacOS)

## Install LLVM for Mac Users

Just use homebrew

```sh
brew install llvm@16
```

LLVM binaries installed via brew can be located from `$(brew --prefix llvm@16)/bin`.

Make sure your LLVM  installed the right one for your architecture. The example shows the output printed from `cmake++` on Apple Silicon M1 machine

```
$ clang++ --version

Homebrew clang version 17.0.6
Target: arm64-apple-darwin23.0.0
Thread model: posix
InstalledDir: /opt/homebrew/opt/llvm/bin
```

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
  echo "Writing data file $FILENAME"
  for (( j=1; j<=LINES; j++ ))
  do
    RANDOM_STRING=$(openssl rand -base64 $LENGTH | tr -dc 'a-zA-Z0-9' | head -c $LENGTH)
    echo $RANDOM_STRING >> $FILENAME
  done
done
```

## Build & Run

Just CMake it with LLVM Clang compiler.

> NOTE: For Mac user, coroutines are supported since C++20 onwards [https://developer.apple.com/xcode/cpp/]. Make sure you have configured PATHS for LLVM, by following the instructions in `brew info llvm`, if it is installed via Homebrew.

### a) Intel

```sh
./build-apple-x86.sh
```

### b) Apple M1

The clang compiler for ARM won't recognise `-stdlib=libc++`. Also for ARM, we need to compile a fat binary.

Before proceeding, you can check the XCode SDK path with:

```sh
xcrun --show-sdk-path
```

Then compile on ARM with:

```sh
./build-apple-m1.sh
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

## References

- Check which compilers on which platforms support parallel execution from [https://en.cppreference.com/w/cpp/compiler_support/17#C.2B.2B17_library_features]
- Check what C++ features are supported by LLVM Clang compiler from [https://clang.llvm.org/cxx_status.html]

