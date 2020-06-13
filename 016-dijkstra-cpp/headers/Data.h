#pragma once

#include <vector>
#include <map>
#include <set>
#include <string>
#include <iostream>
#include <fmt/format.h>

using namespace std;

struct Path {
  vector<int> steps;
  float sumDistance;
};

struct Graph {
  map<int, map<int, float>> edges; // Directional
  set<int> nodes;

  void add(int v1, int v2, float w){
    nodes.insert(v1);
    nodes.insert(v2);
    if (edges.find(v1) != edges.end()){
      if (edges[v1].find(v2) != edges[v1].end()){
        edges[v1][v2] = w;
      }
      else {
        edges[v1].insert(make_pair(v2, w));
      }
    }
    else {
      map<int, float> newv2;
      newv2.insert(make_pair(v2, w));
      edges.insert(make_pair(v1, newv2));
    }
  }

  Path& findShortest(int v1, int v2){
    // TAOTODO
  }
};

ostream &operator<<(ostream &os, Graph const &g){
  cout << "=== Graph ===" << endl;
  cout << g.nodes.size() << " nodes" << endl;
  cout << g.edges.size() << " edges" << endl;
  unsigned int n=0;
  for (auto const &[k,v] : g.edges){
    for (auto const &[kk,vv] : v){
      ++n;

      fmt::print("... edge #{n} : {v1} -> {w:.1f} -> {v2} \n",
        fmt::arg("n", n),
        fmt::arg("v1", k),
        fmt::arg("w", vv),
        fmt::arg("v2", kk)
      );
    }
  }
};

ostream &operator<<(ostream &os, Path const &p){
  string s = fmt::format("{:2f} : ", p.sumDistance);
  for (auto &c : p.steps){
    s += fmt::format("{} -> ", c);
  }
  cout << s << endl;
};

