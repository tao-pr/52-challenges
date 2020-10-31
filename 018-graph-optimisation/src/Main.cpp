#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <iterator>

// Following imports are for stacktracing
#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <filesystem>
namespace fs = std::filesystem;

#include "Base.hpp"
#include "parser.hpp"

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
  cout << "----------------------" << endl;
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

  g.delNode("stop-2");

  assert(g.numNodes() == 3);
  assert(g.numEdges() == 2);

  cout << "All tests DONE" << endl;
  cout << "----------------------" << endl;
}

Graph readRoutesFromFile(string filename){
  const char* lpstrHome = getenv("HOME");
  fs::path pathHome(lpstrHome);
  fs::path pathData("data");
  fs::path pathFlightRoutes("flight-routes");
  fs::path pathFileName(filename);
  fs::path pathFile = pathHome / pathData / pathFlightRoutes / pathFileName;

  cout << "Reading source file : " << pathFile << endl;

  ifstream f(pathFile);
  aria::csv::CsvParser csvParser(f);

  bool isHeader = true;
  cout << "Parsing each line" << endl;
  for (auto& row : csvParser){
    if (isHeader){
      // Skip header row
      isHeader = false;
      continue;
    }
    // Fields: airline,airline ID, source airport, source airport id, 
    //         destination apirport, destination airport id, codeshare, 
    //         stops, equipment
    int fieldId = 0;
    string airline, src, dest, codeshare;
    int numStops;
    for (auto& field : row){

      if (fieldId==0)
        airline = field;
      else if (fieldId==2)
        src = field;
      else if (fieldId==4)
        dest = field;
      else if (fieldId==6)
        codeshare = field;
      else if (fieldId==7)
        numStops = stoi(field);

      cout << "airline = " << airline << ", "
        << "from = " << src << ", "
        << "to = " << dest << ", "
        << "code = " << codeshare << ", "
        << "stops = " << numStops << endl;

      fieldId ++;
    }
  }
  cout << "Finalising graph" << endl;

  Graph g;
  return g;
}

int main(int argc, char** argv){

  signal(SIGSEGV, segFaultHandler);

  runTest();

  // TAOTODO Read route files(s)
  auto g = readRoutesFromFile("routes.csv");

  // TAOTODO
}