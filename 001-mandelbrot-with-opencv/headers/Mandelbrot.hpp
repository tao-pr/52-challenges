#pragma once

#include <string>
#include <vector>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

class Mandelbrot
{
private:
protected:
public:
  Mandelbrot(int nMaxIters=10);
  ~Mandelbrot() {};

  void render(Size& size);
};