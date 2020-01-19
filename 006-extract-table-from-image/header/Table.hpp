#ifndef TABLE_HPP
#define TABLE_HPP

#include <string>
#include <vector>

using namespace std;

/**
 * Extracted table information
 */
struct Table {
  Rect region;
  set<int> verticals;
  set<int> horizontals;

  void drawTo(Mat& im) const 
  {
    rectangle(im, region.tl(), region.br(), Scalar(235,235,235), -1);
  };
};


#endif