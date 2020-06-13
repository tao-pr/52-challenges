#pragma once

#include <limits>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <tuple>
#include <string>
#include <iostream>
#include <fmt/format.h>

using namespace std;

#define NODE tuple<int,double>

struct Path {
  vector<int> steps;
  float sumDistance;
  Path(){
    sumDistance = 0;
  }
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

  float findConnection(int v1, int v2){
    if (v1==v2)
      return 0;
    else if (edges.find(v1)==edges.end())
      return numeric_limits<float>::max();
    else if (edges[v1].find(v2)==edges[v1].end())
      return numeric_limits<float>::max();
    else
      return edges[v1][v2];
  }

  Path& findShortest(int v1, int v2){
    auto comp = [](NODE n1, NODE n2){ return get<1>(n1) > get<1>(n2); };
    priority_queue<NODE, vector<NODE>, decltype(comp)> q(comp);

    // Init Q & distance registry
    map<int, float> distances;
    for (const auto &v : nodes){
      auto d = findConnection(v1,v);
      q.push(make_pair(v, d));
      distances[v] = d;
    }

    // Init steps
    map<int, int> prev;

    // Evaluate each node
    while (!q.empty()){
      auto tu = q.top(); q.pop();
      int v = get<0>(tu);
      float d = get<1>(tu);
      

      // Skip if the distance is not up-to-date
      if (d != distances[v])
        continue;

      // Evaluate neighbours of v
      if (edges.find(v) != edges.end()){
        for (const auto& nextVW : edges[v]){
          auto next = get<0>(nextVW);
          float w = findConnection(v, next) + d;
          if (distances.find(next)==distances.end() || w<distances[next]){
            distances[next] = w;
            prev[next] = v;
            q.push(make_pair(next, w));
          }
        }
      }
    }

    // Reconstruct the path
    Path path;
    auto v = v2;
    while (v != v1){
      path.steps.push_back(v);
      if (prev.find(v) != prev.end()){
        auto v0 = prev[v];
        path.sumDistance += findConnection(v0,v);
        v = v0;
      }
      else break;
    }
    return path;
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
  return os << "=== End of Graph ===" << endl;
};

ostream &operator<<(ostream &os, Path const &p){
  string s = fmt::format("{:2f} : ", p.sumDistance);
  for (auto &c : p.steps){
    s += fmt::format("{} -> ", c);
  }
  return os << s << endl;
};

