#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>

#include "Julia.hpp"

// REF: https://stackoverflow.com/a/77336/4154262
void exceptionHandle(int sig)
{
  void *array[10];
  size_t size;

  // get void*'s for all entries on the stack
  size = backtrace(array, 10);

  // print out all the frames to stderr
  // fprintf(stderr, "Error: signal %d:\n", sig);
  backtrace_symbols_fd(array, size, STDERR_FILENO);
  exit(1);
}

int main(int argc, char** argv)
{
  signal(SIGSEGV, exceptionHandle);

  int nMaxIters;
  double bound = 1.6;
  double reMin, reMax, imMin, imMax;
  double resolution;

  cout << "Julia set generator" << endl;
  cout << "Please enter the range of Z" << endl;
  cout << endl;
  cout << "Real component from : "; cin >> reMin;
  cout << "Real component to   : "; cin >> reMax;
  cout << "Imaginary component from : "; cin >> imMin;
  cout << "Imaginary component to   : "; cin >> imMax;
  cout << "Resolution : "; cin >> resolution;
  cout << "Num iterations : "; cin >> nMaxIters;

  cout << endl;
  cout << "Generating ..." << endl;
  auto m = JuliaSet(nMaxIters, bound);
  m.render(reMin, reMax, imMin, imMax, resolution);
}