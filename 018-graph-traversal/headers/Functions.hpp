#pragma once

#ifndef FF_HPP
#define FF_HPP

#include <tuple>

using namespace std;

double inline distance(tuple<double,double> p1, tuple<double,double> p2){
  // Haversine
  const double R = 6371e3;
  double pp = M_PI / 180;
  double phi1 = get<0>(p1) * pp;
  double phi2 = get<0>(p2) * pp;
  double deltaPhi = (get<0>(p2) - get<0>(p1)) * pp;
  double deltaLambda = (get<1>(p2) - get<1>(p1)) * pp;
  double a = sin(deltaPhi/2) * sin(deltaPhi/2) +
    cos(phi1) * cos(phi2) *
    sin(deltaLambda/2) * sin(deltaLambda/2);
  double c = 2 * atan2(sqrt(a), sqrt(1-a));
  return R * c * 0.001; // km
}

#endif