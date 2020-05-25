#ifndef DATA_H
#define DATA_H

#include <string>
#include <vector>

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

struct Product {
  int           index;
  string        title;
  unsigned int  qty;
  vector<Color> colors;
};


#endif