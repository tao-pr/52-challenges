#pragma once

#include <math.h>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

namespace Cx
{
  Complex<double> sqr(Complex<double>& z)
  {
    return Complex<double>(z.re*z.re - z.im*z.im, 2*z.re*z.im);
  }

  double abs(Complex<double> &z)
  {
    return sqrt(z.re*z.re + z.im*z.im);
  }
};