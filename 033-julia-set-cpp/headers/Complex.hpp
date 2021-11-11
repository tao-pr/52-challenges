#ifndef COMPLEX_HPP
#define COMPLEX_HPP

#include <math.h>

using namespace cv;

namespace Cx
{
  inline Complex<double> zero = Complex<double>(0,0);

  inline Complex<double> sqr(Complex<double>& z)
  {
    return Complex<double>(z.re*z.re - z.im*z.im, 2*z.re*z.im);
  }

  inline double abs(Complex<double> &z)
  {
    return sqrt(z.re*z.re + z.im*z.im);
  }
};

#endif