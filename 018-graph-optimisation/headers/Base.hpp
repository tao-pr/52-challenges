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
  map<string, Edge> edges;
};

struct Edge {
  double cost;
  shared_ptr<Node> from;
  shared_ptr<Node> to;
};

class Graph {
  protected:
    map<string, shared_ptr<Node>> nodes;
};
