#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <iterator>

// Following imports are for stacktracing
#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>

#include "Data.h"

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

  cout << "Dijkstra ..." << endl;

  // Read args
  vector<string> args;
  if (argc > 1){
    args.assign(argv+1, argv+argc);
  }

  // Inputs
  auto g = Graph();
  string input = "";
  if (args.size()>0 && args[0] == "PREDEF"){
    g.add(0,1,1);
    g.add(0,2,2);
    g.add(1,3,5);
    g.add(2,3,1);
  }
  else {
    cout << endl << "NOTE: Enter [n] to finish" << endl;
    while (input != "n"){
      cout << endl << "Input edge (v1,v2,w): ";
      getline(cin, input);
      if (input != "n"){
        stringstream ss(input);
        vector<string> chunks;
        char part = 0;
        int v1, v2;
        double w;
        string substr;
        while (getline(ss, substr, ',')){
          if (part==0){
            // v1
            v1 = stoi(substr);
          }
          else if (part==1){
            // v2
            v2 = stoi(substr);
          }
          else {
            // weight
            w = stof(substr);
          }
          ++part;
        }
        g.add(v1, v2, w);
      }
    }
  }

  cout << "Input complete " << endl;
  cout << g << endl;

  // Verify if the graph is strongly connected
  cout << "Graph strongly connected : " << g.isStronglyConnected() << endl;

  input = "";

  while (input != "n"){
    cout << endl << "Find shortest path from, to : ";
    getline(cin, input);
    if (input != "n"){
      stringstream ss(input);
      vector<string> chunks;
      char part = 0;
      int v1, v2;
      string substr;
      while (getline(ss, substr, ',')){
        if (part==0){
          v1 = stoi(substr);
        }
        else {
          v2 = stoi(substr);
        }
        ++part;
      }
      cout << g.findShortest(v1, v2) << endl;
    }
  }
}

