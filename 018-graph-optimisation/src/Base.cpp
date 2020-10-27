#include "Base.hpp"

Graph::Graph(){

}

Graph::~Graph(){

}

bool Graph::addNode(string value, double cost){
  if (this->nodes.find(value) == this->nodes.end()){
    Node n {.value = value, .cost = cost };
    this->nodes.insert_or_assign(value, n);
    return true;
  }
  else return false;
}

bool Graph::delNode(string value){
  auto it = this->nodes.find(value);
  if (it == this->nodes.end()){
    return false;
  }
  else {
    // Delete the node from map registry
    this->nodes.erase(it);
    return true;
  }
}

bool Graph::addEdge(string from, string to, double cost){
  // NOTE: Will update if already exists
  auto itFrom = this->nodes.find(from);
  auto itTo = this->nodes.find(to);

  if ((itFrom == this->nodes.end()) || (itTo == this->nodes.end())){
    // Either end of the edge does not exist
    return false;
  }
  else {
    (*itFrom).second.edges.insert_or_assign(to, cost);
    return true;
  }
}
