# NOTE: minimum CMake which supports ARM on MacOS is 3.19
cmake_minimum_required(VERSION 3.27)

# Make linking libraries work on MacOS (Arm64 M1)
# https://stackoverflow.com/a/53635241/4154262
set(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")

project("043" LANGUAGES CXX C) # CXX C
set(TARGET_APP "m43")

message(STATUS "Compiler ID: ${CMAKE_CXX_COMPILER_ID}")

find_package(LLVM REQUIRED CONFIG)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")
message(STATUS "Including headers from: ${LLVM_INCLUDE_DIRS}")
message(STATUS "Linking libraries from: ${LLVM_LIBRARY_DIRS}")

# Dependencies
# include_directories($ENV{LLVM_INCLUDE_DIR})
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/hpp")
# link_directories($ENV{LLVM_LIBRARY_DIRS})

# Source files
message("Including source dir: ${CMAKE_CURRENT_SOURCE_DIR}")
file(GLOB SOURCES 
  "${CMAKE_CURRENT_SOURCE_DIR}/hpp/*.hpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
)
set(APP_SRC src/Main.cpp)

# Executable
add_executable(${TARGET_APP} ${SOURCES})
set_target_properties(${TARGET_APP} PROPERTIES 
  OUTPUT_NAME "m43"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin")

# Find LLVM libraries for linker
# llvm_map_components_to_libnames(llvm_libs support core)

# Link with LLVM libraries
# NOTE: Typical:
# target_link_libraries( ${TARGET_APP} ${BUILD_DEPENDENCIES})
message(STATUS "Linking LLVM libraries: ${llvm_libs}")
target_link_libraries( ${TARGET_APP} ${llvm_libs})

message(STATUS "Build output : ${CMAKE_BINARY_DIR}")
