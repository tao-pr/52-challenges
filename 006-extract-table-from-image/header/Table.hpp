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
  vector<Table> children;
};


#endif