#ifndef EXTRACT_
#define EXTRACT_

#include <stdlib.h>
#include <unistd.h>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "Extractor.hpp"

int main(int argc, char** argv)
{
  // Read in the image
  Mat im = imread("./data/20200117134920228.jpg", IMREAD_GRAYSCALE);
  imshow("original", im);
  moveWindow("original", 0, 0);


  waitKey(0);
}

#endif