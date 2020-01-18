cmake_minimum_required(VERSION 3.8)

# Dependencies
include_directories(/usr/local/include)
include_directories("$ENV{OPENCV_INCLUDE_DIR}")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/header")
link_directories(/usr/local/lib)
link_directories("$ENV{OPENCV_LIB_DIR}")

project("006-extract" CXX C)

set(TARGET_APP "extract")

# Source files
file(GLOB SOURCES 
  "${CMAKE_CURRENT_SOURCE_DIR}/header/*.hpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
)
set(APP_SRC src/Main.cpp)

# Third-party dependencies
set(BUILD_DEPENDENCIES 
  opencv_core 
  opencv_imgproc 
  opencv_video
  opencv_videoio
  opencv_features2d 
  opencv_ml 
  opencv_highgui
  opencv_imgcodecs 
  opencv_objdetect
  opencv_xfeatures2d)


# Targets to build
add_executable(${TARGET_APP} ${SOURCES})
set_target_properties(${TARGET_APP} PROPERTIES 
  OUTPUT_NAME "extract"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/build")

# Build recipe
target_link_libraries( ${TARGET_APP} ${BUILD_DEPENDENCIES})

message(STATUS "OUTPUT binary objects  : ${CMAKE_BINARY_DIR}")