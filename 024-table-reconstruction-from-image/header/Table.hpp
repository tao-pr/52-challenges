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
    for (auto v : verticals)
    {
      line(im, Point(v, region.y), Point(v, region.y+region.height), Scalar(70,70,70));
    }

    for (auto h : horizontals)
    {
      line(im, Point(region.x, h), Point(region.x+region.width, h), Scalar(70,70,70));
    }
  };
};


#endif