#include "Base.hpp"

ostream & operator << (ostream &out, const Path &p){
  string str;
  for (auto s : p.stops){
    if (str.size()>0) str += " -> ";
    str += s;
  }
  return out << "Path : " << str << " [sum distance = " << p.sumCost << " km]";
};

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

void Graph::assignNode(string value, Node& n){
  this->nodes.insert_or_assign(value, n);
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

bool Graph::setNodeCost(string node, double cost){
  auto n = this->nodes.find(node);
  if (n != this->nodes.end()){
    n->second.cost = cost;
  }
  else return false;
}

int Graph::numNodes() const{
  return this->nodes.size();
}

int Graph::numEdges() const{
  int num = 0;
  for (auto& n : this->nodes){
    for (auto& e : n.second.edges){
      // Only count valid edges
      auto to = e.first;
      if (this->nodes.find(to) != this->nodes.end()){
        num++;
      }
    }
  }
  return num;
}

Graph Graph::subgraph(set<string> nodes) const {
  Graph subgr;
  for (auto n : nodes){
    auto node = this->getNode(n);
    if (node != nullopt)
      subgr.addNode(node.value().value, node.value().cost);
    else 
      cerr << "Node " << n << " not found in the graph" << endl;
  }
  // Only collect edges which link nodes in subgraph
  for (auto from : nodes){
    for (auto e : this->getEdges(from)){
      auto target = e.first;
      if (nodes.find(target) != nodes.end()){
        subgr.addEdge(from, target, e.second);
      }
    }
  }
  return subgr;
}

vector<string> Graph::getNodes() const{
  vector<string> v;
  for (auto& n : this->nodes){
    v.push_back(n.first);
  }
  return v;
}

map<string, double> Graph::getEdges(string from) const {
  map<string, double> edges;
  auto node = this->nodes.find(from);
  if (node != this->nodes.end()){
    for (auto& e : node->second.edges){
      // Only take valid edges
      auto to = e.first;
      if (this->nodes.find(to) != this->nodes.end()){
        edges.insert_or_assign(to, e.second);
      }
    }
  }
  return edges;
}

optional<Node> Graph::getNode(string node) const {
  auto n = this->nodes.find(node);
  if (n != this->nodes.end()){
    return { n->second };
  }
  else return nullopt;
}

priority_queue<
  NodeInt,
  vector<NodeInt>, 
  NodeIntDesc> 
Graph::mostOutbounds() const {
  priority_queue<
    NodeInt,
    vector<NodeInt>,
    NodeIntDesc> q;
  for (auto& n : this->nodes){
    int numOutflow = this->getEdges(n.first).size();
    q.push(make_tuple(n.first, numOutflow));
  }
  return q;
}

priority_queue<
  NodeInt,
  vector<NodeInt>, 
  NodeIntDesc> 
Graph::mostInbounds() const {
  priority_queue<
    NodeInt,
    vector<NodeInt>,
    NodeIntDesc> q;

  map<string, int> bounds;

  for (auto& n : this->nodes){
    for (auto& e : this->getEdges(n.first)){
      auto dest = e.first;
      auto b = bounds.find(dest);
      if (b != bounds.end()){
        bounds.insert_or_assign(dest, b->second+1);
      }
      else bounds.insert_or_assign(dest, 1);
    }
  }
  for (auto& b : bounds){
    q.push(make_tuple(b.first, b.second));
  }
  return q;
}

double Graph::getDistance(string from, string to) const {
  auto nodeFrom = this->getNode(from).value();
  auto nodeTo = this->getNode(to).value();
  return distance(
    make_tuple(nodeFrom.lat, nodeFrom.lng),
    make_tuple(nodeTo.lat, nodeTo.lng));
}

vector<Path> Graph::expandReach(string to, int maxDegree, double maxCost, vector<Path> paths) {
  // DFS
  vector<Path> out;
  for (auto& path : paths){
    if (path.stops.back()==to){
      out.push_back(path);
    }
    else if (path.stops.size()<maxDegree && path.sumCost<maxCost) {
      // Expand
      auto stop = path.stops.back();
      auto prevStop = path.stops.size()>1 ? path.stops[path.stops.size()-2] : stop;
      auto n = this->getNode(stop).value();
      for (auto &e : n.edges){
        // Do not backtrack
        if (e.first==prevStop)
          continue;
        auto next = e.first;
        auto nextPath = path.clone();

        // Next step of the path
        nextPath.stops.push_back(next);
        nextPath.sumCost += this->getDistance(stop, next);

        // Do not go beyond max cost
        if (nextPath.sumCost > maxCost)
          continue;

        if (next==to){
          // Found the end!
          out.push_back(nextPath);
        }
        else {
          // Go deeper!
          vector<Path> tPaths{ nextPath };
          auto expandedPaths = this->expandReach(to, maxDegree, maxCost, tPaths);
          for (auto& p : expandedPaths){
            out.push_back(p);
          }
        }
      }
    }
  }
  return out;
}

Graph Graph::reversed() const {
  Graph g;
  for (auto& n : this->nodes){
    auto n_ = n.second.cloneWithoutEdges();
    g.assignNode(n.first, n_);
  }
  // Add all edges in reverse
  for (auto& source : this->nodes){
    for (auto& e : source.second.edges){
      auto target = e.first;
      g.addEdge(target, source.first, e.second);
    }
  }
  return g;
}

set<string> Graph::traverse(string from, const set<string> &skip) const {
  set<string> visited;
  for (const auto n : skip)
    visited.insert(n);
  const auto node = this->nodes.find(from);
  if (node == this->nodes.end())
    return visited;
  for (const auto& e : node->second.edges){
    if (skip.find(e.first) == skip.end()){
      visited.insert(e.first);
      // DFS into
      visited = traverse(e.first, visited);
    }
  }
  return visited;
}

bool Graph::isAllNodesTravesableFrom(string from) const {
  auto visited = traverse(from, set<string>{from});

  // Check if all nodes are visited

  // TAOTODO;

  return false;
}

bool Graph::isStronglyConnected() const {
  // Korasaju's algo
  auto from = *this->nodes.cbegin();
  if (!isAllNodesTravesableFrom(from.first))
    return false;
  if (!this->reversed().isAllNodesTravesableFrom(from.first))
    return false;
  return true;
}