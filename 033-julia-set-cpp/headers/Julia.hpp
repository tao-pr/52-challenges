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
  JuliaSet(int nMaxIters=10, double bound=2);
  virtual int convergence(Complex<double>& z, Complex<double>& c, int nIter=0) const = 0;

public:
  ~JuliaSet() {};

  void render(double reMin, double reMax, double imMin, double imMax, double resolution) const;
};

class MandelbrotSet : public JuliaSet 
{
protected:
  int convergence(Complex<double>& z, Complex<double>& c, int nIter=0) const;
public:
  MandelbrotSet(int nMaxIters=10, double bound=2);
};


#endif