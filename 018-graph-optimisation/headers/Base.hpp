#pragma once

#include <memory>
#include <vector>
#include <stack>
#include <map>
#include <string>
#include <iostream>
#include <fmt/format.h>

using namespace std;

struct Node {
  string value;
  double cost;
  map<string, double> edges;
};

class Graph {
  protected:
    map<string, Node> nodes;

  public:
    Graph();
    ~Graph();

    // Modifiers
    bool addNode(string value, double cost);
    bool delNode(string value);
    bool addEdge(string from, string to, double cost);
    bool setNodeCost(string node, double cost);

    // Getters
    int numNodes() const;
    int numEdges() const;
    vector<string> getNodes() const;
    map<string, double> getEdges(string from) const;
    Node& getNode(string node) const;
};
