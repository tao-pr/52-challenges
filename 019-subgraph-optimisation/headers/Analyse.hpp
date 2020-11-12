#pragma once

#include "Base.hpp"

void analyse(Graph& g);
void topOutbounds(Graph& g, int num);
void topInbounds(Graph& g, int num);
void findReachability(Graph& g, string from, string to, int maxDegree, double maxDistance);
void analyseSubgraph(Graph&g, set<string> airports);