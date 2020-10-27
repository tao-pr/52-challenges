#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <iterator>

// Following imports are for stacktracing
#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>

#include "Base.hpp"
#include "Test.hpp"

using namespace std;

// @href https://stackoverflow.com/questions/77005/how-to-automatically-generate-a-stacktrace-when-my-gcc-c-program-crashes
inline void segFaultHandler(int sig) {
  void *array[10];
  size_t size;

  // get void*'s for all entries on the stack
  size = backtrace(array, 10);

  // print out all the frames to stderr
  fprintf(stderr, "Error: signal %d:\n", sig);
  backtrace_symbols_fd(array, size, STDERR_FILENO);
  exit(1);
}

int main(int argc, char** argv){

  signal(SIGSEGV, segFaultHandler);

  // TAOTODO
}