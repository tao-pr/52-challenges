#include "Analyse.hpp"

void analyse(Graph& g){
  topOutbounds(g, 10);
  topInbounds(g, 10);
}

void topOutbounds(Graph& g, int num){
  cout << "----------------------" << endl;
  cout << "Top " << num << " Outbound routes" << endl;
  int i=0;
  auto Outbounds = g.mostOutbounds();
  while (i < num){
    ++i;
    auto el = Outbounds.top();
    cout << "   [" << i << "] " << get<0>(el) << " : " << get<1>(el) << " Outbounds" << endl;
    Outbounds.pop();
  }
}

void topInbounds(Graph& g, int num){
  cout << "----------------------" << endl;
  cout << "Top " << num << " Inbound routes" << endl;
  int i=0;
  auto Inbounds = g.mostInbounds();
  while (i < num){
    ++i;
    auto el = Inbounds.top();
    cout << "   [" << i << "] " << get<0>(el) << " : " << get<1>(el) << " Inbounds" << endl;
    Inbounds.pop();
  }
}