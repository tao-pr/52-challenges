# Kalman Filter tracking video

## Prerequisites

- First of all, you need a C++20 compatible GCC compiler.

- Install [itertools](https://github.com/ryanhaining/cppitertools)

```bash
mkdir -p headers/itertools
cd headers/itertools
git clone --depth 1 git@github.com:ryanhaining/cppitertools.git
cd -
```

- Download a dashcam video samples, i.e. from https://www.pexels.com/video/driving-fast-on-an-empty-highway-5608186/ 
into `/media/video.mp4`

## Build and Run

Just simply execute the make script and run

```bash
./make.sh
./build/prototype # run
```


## Licence

MIT