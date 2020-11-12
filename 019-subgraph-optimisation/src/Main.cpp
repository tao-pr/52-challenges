#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <iterator>
#include <math.h>

// Following imports are for stacktracing
#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <filesystem>
namespace fs = std::filesystem;

#include "Base.hpp"
#include "Analyse.hpp"
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

  g.setNodeCost("stop-2", 15);

  assert(g.getNode("stop-2").value().cost == 15);

  g.delNode("stop-2");

  assert(g.numNodes() == 3);
  assert(g.numEdges() == 2);

  // Just add a new temp edge for test
  g.addEdge("start", "end", 5);
  assert(g.getEdge("start", "end").value() == 5);
  // remove the added temp edge
  g.delEdge("start", "end");
  assert(g.getEdge("start", "end") == nullopt);


  set<string> nodes {"stop-1", "end"};
  auto subg = g.subgraph(nodes);
  assert(subg.numNodes() == 2);
  auto _nodes = subg.getNodes();
  assert(find(_nodes.begin(), _nodes.end(), "stop-1") != _nodes.end());
  assert(find(_nodes.begin(), _nodes.end(), "end") != _nodes.end());
  assert(find(_nodes.begin(), _nodes.end(), "start") == _nodes.end());
  for (auto &n : _nodes){
    for (auto &e : subg.getEdges(n)){
      assert(find(nodes.begin(), nodes.end(), e.first) != nodes.end());
    }
  }

  // Original graph should not be strongly connected
  assert(g.isStronglyConnected() == false);
  // Add one more link from end -> start should make it
  g.addEdge("end", "start", 1);
  assert(g.isStronglyConnected() == true);

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

  Graph g;

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

      // cout << "airline = " << airline << ", "
      //   << "from = " << src << ", "
      //   << "to = " << dest << ", "
      //   << "code = " << codeshare << ", "
      //   << "stops = " << numStops << endl;

      g.addNode(src, 0);
      g.addNode(dest, 0);
      g.addEdge(src, dest, numStops+1);

      fieldId ++;
    }
  }
  cout << "----------------------------" << endl;
  cout << "Finalising graph" << endl;
  cout << "Num nodes = " << g.numNodes() << endl;
  cout << "Num edges = " << g.numEdges() << endl;
  cout << "----------------------------" << endl;
  return g;
}

Graph readAirportsFromFile(string filename, Graph &g){

  const char* lpstrHome = getenv("HOME");
  fs::path pathHome(lpstrHome);
  fs::path pathData("data");
  fs::path pathFlightRoutes("flight-routes");
  fs::path pathFileName(filename);
  fs::path pathFile = pathHome / pathData / pathFlightRoutes / pathFileName;

  ifstream f(pathFile);
  aria::csv::CsvParser csvParser(f);

  cout << "Reading source file : " << pathFile << endl;

  bool isHeader = true;
  cout << "Parsing each line" << endl;
  for (auto& row : csvParser){
    if (isHeader){
      // Skip header row
      isHeader = false;
      continue;
    }
    // Fields: id, fullname, city, country, code, code2, lat, lng, ...
    int fieldId = 0;
    string fullname, city, country, code;
    double lat, lng;
    for (auto& field : row){

      if (fieldId==1)
        fullname = field;
      else if (fieldId==2)
        city = field;
      else if (fieldId==3)
        country = field;
      else if (fieldId==4)
        code = field;
      else if (fieldId==6)
        lat = stod(field);
      else if (fieldId==7)
        lng = stod(field);
      fieldId++;

      // Find and update the node
      auto node = g.getNode(code);
      if (node != nullopt){
        auto v = node.value();
        v.lat = lat;
        v.lng = lng;
        v.note = city + ", " + country;
        g.assignNode(code, v);
      }
    }
  }

  return g;
}

Graph updateRouteDistances(Graph& g){
  cout << "Updating edge distances ... " << endl;
  // Update route distances as edge cost
  for (auto n : g.getNodes()){
    auto from = g.getNode(n).value();
    vector<tuple<string,double>> updateList;
    for (auto e : from.edges){
      auto to = g.getNode(e.first).value();
      auto posFrom = make_tuple(from.lat, from.lng);
      auto posTo = make_tuple(to.lat, to.lng);
      auto dist = distance(posFrom, posTo);
      updateList.push_back(make_tuple(e.first, dist));
    }
    for (auto e : updateList){
      g.addEdge(from.value, get<0>(e), get<1>(e));
    }
  }
  cout << "[DONE]" << endl;
  return g;
}


int main(int argc, char** argv){

  signal(SIGSEGV, segFaultHandler);

  runTest();

  auto g = readRoutesFromFile("routes.csv");
  g = readAirportsFromFile("airports-extended.csv", g);
  g = updateRouteDistances(g);
  analyse(g);
}