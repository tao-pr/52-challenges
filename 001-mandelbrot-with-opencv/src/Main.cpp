#include "Mandelbrot.hpp"

int main(int argc, char** argv)
{
  int nMaxIters = 30;
  double bound = 1.6;
  double reMin, reMax, imMin, imMax;
  double resolution;

  cout << "Mandelbrot generator" << endl;
  cout << "Please enter the range of Z" << endl;
  cout << endl;
  cout << "Real component from : "; cin >> reMin;
  cout << "Real component to   : "; cin >> reMax;
  cout << "Imaginary component from : "; cin >> imMin;
  cout << "Imaginary component to   : "; cin >> imMax;
  cout << "Resolution : "; cin >> resolution;

  cout << endl;
  cout << "Generating ..." << endl;
  auto m = Mandelbrot(nMaxIters, bound);
  m.render(reMin, reMax, imMin, imMax, resolution);
}