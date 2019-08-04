#ifndef MANDELBROT_HPP
#define MANDELBROT_HPP

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
  Mandelbrot(){};
  int convergence(Complex<double>& z, Complex<double>& c, int nIter=0) const;

protected:
  int nMaxIters;
  double bound;

public:
  Mandelbrot(int nMaxIters=10, double bound=2);
  ~Mandelbrot() {};

  void render(double reMin, double reMax, double imMin, double imMax, double resolution) const;
};

#endif