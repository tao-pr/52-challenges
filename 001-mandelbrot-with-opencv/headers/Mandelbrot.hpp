#pragma once

#include <string>
#include <vector>

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "Complex.hpp"

using namespace cv;
using namespace std;

class Mandelbrot
{
private:
  bool isConverge(Complex<double>& z) const;

protected:
  int nMaxIters;

public:
  Mandelbrot(int nMaxIters=10);
  ~Mandelbrot() {};

  void render(Size& size, Rect range=Rect(-5,-5,10,10)) const;
};