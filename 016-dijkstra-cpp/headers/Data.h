#pragma once

#include <vector>
#include <map>
#include <string>
#include <iostream>

using namespace std;

struct Graph {
  map<int, map<int, float>> edges; // Directional
  map<int, string> nodes;
};

ostream &operator<<(ostream &os, Graph const &g){
  cout << "=== Graph ===" << endl;
  cout << g.nodes.size() << " nodes" << endl;
  cout << g.edges.size() << " edges" << endl;
  unsigned int n=0;
  for (auto const &[k,v] : g.edges){
    for (auto const &[kk,vv] : v){
      ++n;
      cout << "... edge #" << n << " : " << k << " -> " 
        << "WEIGHT" << " -> " << kk << endl;
    }
  }
};

