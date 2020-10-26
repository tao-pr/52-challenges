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

    bool addNode(string value, double cost);
    bool delNode(string value);
    bool addEdge(string from, string to, double cost);
};
