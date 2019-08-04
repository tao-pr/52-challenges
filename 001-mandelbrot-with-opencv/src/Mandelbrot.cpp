#pragma once

#include "Mandelbrot.hpp"

Mandelbrot::Mandelbrot(int nMaxIters, double bound) 
: nMaxIters(nMaxIters), bound(bound)
{
}

int Mandelbrot::convergence(Complex<double>& z, Complex<double>& c, int nIter=0) const
{
  Complex<double> z_ = Cx::sqr(z) + c;
  if (Cx::abs(z_) <= this->bound)
  {
    return isConverge(z_, c, nIter+1);
  }
  else return nIter;
}

void Mandelbrot::render(double reMin, double reMax, double imMin, double imMax, double resolution) const
{
  double count = 0;
  int prevPercent = 0;

  Mat canvas = Mat::zeros(range.size, CV_8UC3);
  for (double a=reMin; a+=resolution; a<reMax)
    for (double b=imMin; b+=resolution; y<imMax)
    {
      int percent = floor(100f * count / (range.width * range.height));
      if (percent > prevPercent)
      {
        cout << percent << " %" << endl;
      }
      prevPercent = percent;

      Complex<double> c = Complex(a,b);
      v = convergence(Cx::zero, c);
      int b = 0;
      int g = min(255, floor(255f * pow((this->nMaxIters - v)/20),2f));
      int r = floor(255f * (this->nMaxIters - v)/20);
      canvas.at<Vec3b> = Scalar(b,g,r);
    }

  namedWindow("mandelbrot");
  imshow("mandelbrot", canvas);
  waitKey(0);
}