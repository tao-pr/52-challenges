#include "Analyse.hpp"

void analyse(Graph& g){
  topOutbounds(g, 10);
  topInbounds(g, 10);
  findReachability(g, "FRA", "BKK", 3, numeric_limits<double>::infinity());
  findReachability(g, "HKG", "KIX", 3, 4000);
  analyseSubgraph(g, set<string>{"FRA", "MUC", "LHR", "PMI"});
  analyseSubgraph(g, set<string>{"MUC", "CNX", "BKK"});
}

void topOutbounds(Graph& g, int num){
  cout << "----------------------" << endl;
  cout << "Top " << num << " Outbound routes" << endl;
  int i=0;
  auto outbounds = g.mostOutbounds();
  while (i < num){
    ++i;
    auto el = outbounds.top();
    string cityCountry = g.getNode(get<0>(el)).value().note;
    cout << "   [" << i << "] " << get<0>(el) << 
      "(" << cityCountry << ") : " << get<1>(el) << " outbounds" << endl;
    outbounds.pop();
  }

  while (outbounds.size() > 1)
    outbounds.pop();

  auto least = outbounds.top();
  cout << "Least outbound = " << get<0>(least) << " : only " << get<1>(least) << " outbounds" << endl;
}

void topInbounds(Graph& g, int num){
  cout << "----------------------" << endl;
  cout << "Top " << num << " Inbound routes" << endl;
  int i=0;
  auto inbounds = g.mostInbounds();
  while (i < num){
    ++i;
    auto el = inbounds.top();
    string cityCountry = g.getNode(get<0>(el)).value().note;
    cout << "   [" << i << "] " << get<0>(el) <<
      "(" << cityCountry << ") : " << get<1>(el) << " inbounds" << endl;
    inbounds.pop();
  }

  while (inbounds.size() > 1)
    inbounds.pop();

  auto least = inbounds.top();
  cout << "Least inbound = " << get<0>(least) << " : only " << get<1>(least) << " inbounds" << endl;
}

void findReachability(Graph& g, string from, string to, int maxDegree, double maxDistance){
  cout << "----------------------" << endl;
  cout << "Finding all reachabilities from : " <<
    from << " -> " << to << endl;

  vector<string> s {from};
  Path p {.stops = s, .sumCost = 0 };
  vector<Path> paths {p};
  paths = g.expandReach(to, maxDegree, maxDistance, paths);

  // Sort the path by distance
  priority_queue<Path, vector<Path>, Path> q;
  for (auto& p : paths)
    q.push(p);

  while (q.size()>0){
    auto p = q.top();
    cout << p << endl;
    q.pop();
  }
}

void analyseSubgraph(Graph&g, set<string> airports){
  cout << "----------------------" << endl;
  cout << "Analysing subgraph : ";
  string str = "";
  for (auto a : airports)
    if (str.size()>0)
      str += ", " + a;
    else 
      str = a;
  cout << str << endl;

  auto subgraph = g.subgraph(airports);
  if (subgraph.isStronglyConnected()){
    cout << "(Graph is strongly connected)" << endl;
    // Examine which edge gets removed will make the subgraph 
    // NOT strongly connected anymore
    int numRemovable = 0;
    for (auto from : subgraph.getNodes()){
      const auto edges = subgraph.getEdges(from);
      for (auto e : edges){
        const auto w = e.second;
        const auto to = e.first;
        // Test removing this edge
        subgraph.delEdge(from, to);
        if (!subgraph.isStronglyConnected()){
          numRemovable++;
          cout << "... Route " << from << " -> " << to << " CANNOT be removed" << endl;
        }
        else {
          cout << "... Route " << from << " -> " << to << " can be removed. Graph remains strongly connected." << endl;
        }
        // Add the edge back
        subgraph.addEdge(from, to, w);
      }
    }
    if (numRemovable==0)
      cout << "... All routes are removeable individually. Graph will remain strongly connected." << endl;
  }
  else
    cout << "(Graph is NOT strongly connected)" << endl;
}

