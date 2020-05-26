#ifndef DATA_H
#define DATA_H

#include <string>
#include <vector>

using namespace std;

enum Colour {
  None = 0,
  White,
  Green,
  Blue,
  Brown,
  Black,
  Red
};

struct Campaign {
  int           numDays;
  string        title;

  Campaign(int _numDays, string _title){
    numDays = _numDays;
    title   = _title;
  };
};

struct Product {
  int            index;
  string         title;
  unsigned int   qty;
  vector<Colour> colours;
  vector<Campaign> campaigns;
};




#endif