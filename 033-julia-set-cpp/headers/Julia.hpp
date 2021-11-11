#ifndef JULIA_SET
#define JULIA_SET

#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "Complex.hpp"

using namespace cv;
using namespace std;

class JuliaSet
{
private:
  JuliaSet(){};
  int convergence(Complex<double>& z, Complex<double>& c, int nIter=0) const;

protected:
  int nMaxIters;
  double bound;

public:
  JuliaSet(int nMaxIters=10, double bound=2);
  ~JuliaSet() {};

  void render(double reMin, double reMax, double imMin, double imMax, double resolution) const;
};


#endif