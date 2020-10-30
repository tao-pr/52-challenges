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

void runTest(){
  cout << "Running test" << endl;
  Graph g;
  g.addNode("start", 0);
  g.addNode("end", 1);
  g.addNode("stop-1", 3);
  g.addNode("stop-2", 5);
  g.addEdge("start","stop-1", 1);
  g.addEdge("start","stop-2", 2);
  g.addEdge("stop-1","end", 10);
  g.addEdge("stop-2","end", 5);

  assert(g.numNodes() == 4);
  assert(g.numEdges() == 4);
  assert(g.getEdges("stop-1").size() == 1);

  g.addEdge("stop-1", "stop-2", 3);

  assert(g.numNodes() == 4);
  assert(g.numEdges() == 5);
  assert(g.getEdges("stop-1").size() == 2);

  cout << "All tests DONE" << endl;
}

int main(int argc, char** argv){

  signal(SIGSEGV, segFaultHandler);

  runTest();

  // TAOTODO
}