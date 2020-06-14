#pragma once

#include <limits>
#include <vector>
#include <stack>
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
    else if (edges.find(v1)==edges.end()){
      return numeric_limits<float>::max();
    }
    else if (edges[v1].find(v2)==edges[v1].end()){
      return numeric_limits<float>::max();
    }
    else
      return edges[v1][v2];
  }

  Path findShortest(int v1, int v2){
    auto comp = [](NODE n1, NODE n2){ return get<1>(n1) > get<1>(n2); };
    priority_queue<NODE, vector<NODE>, decltype(comp)> q(comp);

    // Init Q & distance registry
    map<int, float> distances;
    for (const auto &v : nodes){
      auto d = findConnection(v1,v);
      cout << "from " << v1 << "->" << v << " = " << d << endl; // TAODEBUG
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
      
      cout << "... Q size : " << q.size() << ", computing " << v << endl; 

      // Skip if the distance is not up-to-date
      if (d != distances[v]){
        cout << "...... skip " << v << ", d=" << d << " but distance registry = " << distances[v] << endl;
        continue;
      }

      // Evaluate neighbours of v
      if (edges.find(v) != edges.end()){
        for (const auto& nextVW : edges[v]){
          auto next = get<0>(nextVW);
          float w = findConnection(v, next) + d;
          if (distances.find(next)==distances.end() || w<distances[next]){
            cout << "...... Updating distance " << v << "->" << next << " => " << w << endl; 
            distances[next] = w;
            prev[next] = v;
            q.push(make_pair(next, w));
          }
        }
      }
    }

    cout << "... All nodes evaluated " << endl;

    // Reconstruct the path
    Path path;
    stack<int> reversePath;
    reversePath.push(v2);
    while (reversePath.top() != v1){
      auto vCurr = reversePath.top();
      auto vPrev = prev[vCurr];
      reversePath.push(vPrev);
      path.sumDistance += findConnection(vPrev, vCurr);
    }

    while (!reversePath.empty()){
      path.steps.push_back(reversePath.top());
      reversePath.pop();
    }

    return path;
  }

  Graph reverse(){
    Graph gr;
    for (const auto &[v1, vnexts] : edges){
      for (const auto &[v2, w] : vnexts){
        gr.add(v2, v1, w);
      }
    }

    return gr;
  }

  void dfs(int v, set<int>& visited){
    // DFS traversal and mark the visited nodes

    // Stop as all nodes are visited
    if (visited.size() == nodes.size() || visited.find(v) != visited.end())
      return;

    // Mark self as visited
    visited.insert(v);
    cout << "... node " << v << " visited" << endl;

    if (edges.find(v) != edges.end())
      for (const auto& [next, w] : edges[v]){
        dfs(next, visited);
        if (visited.size() == nodes.size())
          return;
      }
    else
      return;
  }

  bool isStronglyConnected(){
    set<int> visited;

    // DFS and mark visited nodes
    cout << "... DFS, begins from " << *nodes.begin() << endl; 
    dfs(*nodes.begin(), visited);

    // If all nodes are visited, proceed
    if (visited.size() < nodes.size())
      return false;

    // Reverse the edges and try again
    cout << "... Reversing graph" << endl;
    Graph gr = reverse();

    // DFS and mark visited nodes
    visited.clear();
    cout << "... DFS on reversed graph, begins from " << *nodes.begin() << endl;
    gr.dfs(*gr.nodes.begin(), visited);

    if (visited.size() < nodes.size())
      return false;
    else
      return true;
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
  for (const auto &c : p.steps){
    s += fmt::format("{} -> ", c);
  }
  return os << s << endl;
};

