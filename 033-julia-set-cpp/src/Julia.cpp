#include "Julia.hpp"


JuliaSet::JuliaSet(int nMaxIters, double bound) 
  : nMaxIters(nMaxIters), bound(bound)
{
}

void JuliaSet::render(double reMin, double reMax, double imMin, double imMax, double resolution) const
{
  int prevPercent = -1;

  int w = ceil((reMax - reMin) / resolution)+1;
  int h = ceil((imMax - imMin) / resolution)+1;

  cout << "Size : " << w << " x " << h << endl;

  long tot = w*h;
  long cnt = 0;

  Mat canvas = Mat::zeros(Size(h,w), CV_8UC3);
  for (double a=reMin; a<=reMax; a+=resolution)
    for (double b=imMin; b<=imMax; b+=resolution)
    {
      cnt ++;
      int x = floor((a-reMin)/resolution);
      int y = floor((b-imMin)/resolution);
      int percent = floor(100.0f * cnt / (float)tot);
      auto c = Complex<double>(a,b);
      auto v = convergence(Cx::zero, c);
      int _b = 0;
      int _g = floor(std::min(255.0f, floor(255.0f * powf((this->nMaxIters - v)/20.0f, 2.0f))));
      int _r = floor(255.0f * (this->nMaxIters - v)/20.0f);
      auto& px = canvas.at<Vec3b>(Point(y,x));
      px[2] = _b;
      px[1] = _g;
      px[0] = _r;
      cout << percent << "% : convergence (" << x << ", " << y <<") = " << v << endl; // TAODEBUG:
    }

  cout << "Displaying the results" << endl;
  namedWindow("Julia");
  imshow("Julia", canvas);
  waitKey(0);
}


MandelbrotSet::MandelbrotSet(int nMaxIters, double bound)
  : JuliaSet(nMaxIters, bound)
{
}

int MandelbrotSet::convergence(Complex<double>& z, Complex<double>& c, int nIter) const
{
  Complex<double> z_ = Cx::sqr(z) + c;
  if (Cx::abs(z_) <= this->bound)
  {
    if (nIter + 1 < this->nMaxIters)
      return convergence(z_, c, nIter+1);
    else 
      return nIter+1;
  }
  else return nIter;
}
