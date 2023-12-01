cmake_minimum_required(VERSION 3.8)

# Dependencies
# include_directories(/usr/local/include)
include_directories(/usr/local/opt/llvm/include)
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/hpp")
# link_directories(/usr/local/lib)
link_directories(//usr/local/opt/llvm/lib)

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

# Link lib
target_link_libraries( ${TARGET_APP} ${BUILD_DEPENDENCIES})

message(STATUS "Build output : ${CMAKE_BINARY_DIR}")
