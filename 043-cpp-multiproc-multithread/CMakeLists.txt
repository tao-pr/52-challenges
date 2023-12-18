# NOTE: minimum CMake which supports ARM on MacOS is 3.19
cmake_minimum_required(VERSION 3.27)

find_package(LLVM REQUIRED)

# Dependencies
include_directories($ENV{LLVM_ROOT}/include/)
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/hpp")
link_directories($ENV{LLVM_ROOT}/lib/)

# Project
project("043" CXX C)
set(TARGET_APP "m43")

# Source files
message("Including source dir: ${CMAKE_CURRENT_SOURCE_DIR}")
file(GLOB SOURCES 
  "${CMAKE_CURRENT_SOURCE_DIR}/hpp/*.hpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
)
set(APP_SRC src/Main.cpp)

# Third-party dependencies
# set(BUILD_DEPENDENCIES 
#   libfmt.a)

# Executable
add_executable(${TARGET_APP} ${SOURCES})
set_target_properties(${TARGET_APP} PROPERTIES 
  OUTPUT_NAME "m43"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin")

# Find LLVM libraries for linker
llvm_map_components_to_libnames(llvm_libs support core)

# Link with LLVM libraries
# NOTE: Typical:
# target_link_libraries( ${TARGET_APP} ${BUILD_DEPENDENCIES})
target_link_libraries( ${TARGET_APP} ${llvm_libs})

message(STATUS "Build output : ${CMAKE_BINARY_DIR}")
