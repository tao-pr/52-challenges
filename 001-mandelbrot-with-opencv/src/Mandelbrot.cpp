#pragma once

#include "Mandelbrot.hpp"

Mandelbrot::Mandelbrot(int nMaxIters, double bound) 
: nMaxIters(nMaxIters), bound(bound)
{
}

int Mandelbrot::convergence(Complex<double>& z, Complex<double>& c, int nIter) const
{
  Complex<double> z_ = Cx::sqr(z) + c;
  if (Cx::abs(z_) <= this->bound)
  {
    return convergence(z_, c, nIter+1);
  }
  else return nIter;
}

void Mandelbrot::render(double reMin, double reMax, double imMin, double imMax, double resolution) const
{
  int prevPercent = -1;

  int w = ceil((reMax - reMin) / resolution);
  int h = ceil((imMax - imMin) / resolution);
  int x = 0;
  int y = 0;

  cout << "Size : " << w << " x " << h << endl;

  Mat canvas = Mat::zeros(Size(w,h), CV_8UC3);
  for (double a=reMin; a<=reMax; a+=resolution, x++)
    for (double b=imMin; b<=imMax; b+=resolution, y++)
    {
      int percent = floor(100.0f * (x+y) / (float)(w * h));
      if (percent > prevPercent)
      {
        cout << percent << " %" << endl;
      }
      prevPercent = percent;

      auto c = Complex<double>(a,b);
      auto v = convergence(Cx::zero, c);
      int _b = 0;
      int _g = floor(std::min(255.0f, floor(255.0f * powf((this->nMaxIters - v)/20.0f, 2.0f))));
      int _r = floor(255.0f * (this->nMaxIters - v)/20.0f);
      auto& px = canvas.at<Vec3b>(Point(y,x));
      px[2] = _b;
      px[1] = _g;
      px[0] = _r;
    }

  namedWindow("mandelbrot");
  imshow("mandelbrot", canvas);
  waitKey(0);
}