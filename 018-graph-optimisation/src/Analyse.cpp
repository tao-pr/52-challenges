#include "Analyse.hpp"

void analyse(Graph& g){
  topOutbounds(g, 10);
  topInbounds(g, 10);
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