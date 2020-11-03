#pragma once

#include <optional>
#include <memory>
#include <vector>
#include <stack>
#include <map>
#include <queue>
#include <string>
#include <iostream>
#include <fmt/format.h>

using namespace std;

struct Node {
  string value;
  double cost;
  double lat;
  double lng;
  map<string, double> edges;
};

#define NodeInt tuple<string, int>

struct NodeIntDesc {
  inline bool operator()(NodeInt &a, NodeInt &b){
    return get<1>(a) < get<1>(b);
  }
};

class Graph {
  protected:
    map<string, Node> nodes;

  public:
    Graph();
    ~Graph();

    // Modifiers
    bool addNode(string value, double cost);
    void assignNode(string value, Node& n);
    bool delNode(string value);
    bool addEdge(string from, string to, double cost);
    bool setNodeCost(string node, double cost);

    // Getters
    int numNodes() const;
    int numEdges() const;
    vector<string> getNodes() const;
    map<string, double> getEdges(string from) const;
    optional<Node> getNode(string node) const;

    // Analysis
    priority_queue<
      NodeInt,
      vector<NodeInt>, 
      NodeIntDesc> mostOutbounds() const;
    priority_queue<
      NodeInt,
      vector<NodeInt>, 
      NodeIntDesc> mostInbounds() const;
};
