#ifndef DATA_H
#define DATA_H

#include <string>
#include <vector>
#include <chrono>

using namespace std;

enum Color {
  None = 0,
  White,
  Green,
  Blue,
  Brown,
  Black,
  Red
};

struct Campaign {
  chrono::steady_clock::time_point  dt;
  int                 numDays;
  int                 targetGroup;
  string              title;
};

struct Product {
  int           index;
  string        title;
  unsigned int  qty;
  vector<Color> colors;
  vector<Campaign> campaigns;
};




#endif