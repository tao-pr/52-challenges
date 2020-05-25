cmake_minimum_required(VERSION 3.8)

# Dependencies
include_directories(/usr/local/include)
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/headers")
include_directories("${FLATBUFFER_SRC_DIR}/include/flatbuffers")
link_directories(/usr/local/lib)

project("013-flatbuff" CXX C)

set(TARGET_APP "flatbuff")

# Source files
file(GLOB SOURCES 
  "${CMAKE_CURRENT_SOURCE_DIR}/headers/*.hpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
)
set(APP_SRC src/Main.cpp)

# Third-party dependencies
set(BUILD_DEPENDENCIES)


# Targets to build
add_executable(${TARGET_APP} ${SOURCES})
set_target_properties(${TARGET_APP} PROPERTIES 
  OUTPUT_NAME "flatbuff"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/build")

# Build recipe
target_link_libraries( ${TARGET_APP} ${BUILD_DEPENDENCIES})

message(STATUS "OUTPUT binary objects  : ${CMAKE_BINARY_DIR}")