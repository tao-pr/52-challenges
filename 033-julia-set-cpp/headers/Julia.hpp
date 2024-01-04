#ifndef JULIA_SET
#define JULIA_SET

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "Complex.hpp"

using namespace cv;
using namespace std;

/**
 * Generic Julia set
 */
class JuliaSet
{
protected:
  int nMaxIters;
  double bound;
  Complex<double> c;
  int convergence(Complex<double> &z, int nIter = 0) const;

public:
  JuliaSet(Complex<double> &c, int nMaxIters = 10, double bound = 2);
  ~JuliaSet(){};

  void render(double reMin, double reMax, double imMin, double imMax, double resolution) const;
};

#endif