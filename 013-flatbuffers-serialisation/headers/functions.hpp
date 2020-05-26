#ifndef FUNC_HPP
#define FUNC_HPP

#include <vector>

#include "data.hpp"

using namespace std;

inline vector<Product> generateProducts()
{
  auto products = vector<Product>();
  for (int i=0; i<25; i++){
    products.push_back(Product());
    products[i].index = i;
  }

  auto colourPresets = vector<vector<Colour>>();
  for (int i=0; i<4; i++){
    colourPresets.push_back(vector<Colour>());
  }

  // Initialise colour presets
  colourPresets[0].push_back(White);
  colourPresets[0].push_back(Brown);
  colourPresets[0].push_back(None);
  colourPresets[0].push_back(Green);
  colourPresets[1].push_back(White);
  colourPresets[1].push_back(Green);
  colourPresets[1].push_back(Red);
  colourPresets[1].push_back(None);
  colourPresets[2].push_back(Blue);
  colourPresets[2].push_back(Red);
  colourPresets[2].push_back(Black);
  colourPresets[3].push_back(None);
  colourPresets[3].push_back(White);
  
  // Initialise products
  products[0].title = "Table";
  products[1].title = "Mouse";
  products[2].title = "Keyboard";
  products[3].title = "Glass";
  products[4].title = "Lamp";
  products[5].title = "Watch";
  products[6].title = "Adaptor";
  products[7].title = "Cable";
  products[8].title = "External HDD";

  products[0].qty = 5;
  products[1].qty = 30;
  products[2].qty = 45;
  products[3].qty = 30;
  products[4].qty = 5;
  products[5].qty = 5;
  products[6].qty = 35;
  products[7].qty = 30;
  products[8].qty = 10;

  products[0].colours = colourPresets[0];
  products[1].colours = colourPresets[1];
  products[2].colours = colourPresets[1];
  products[3].colours = colourPresets[0];
  products[4].colours = colourPresets[0];
  products[5].colours = colourPresets[2];
  products[6].colours = colourPresets[0];
  products[7].colours = colourPresets[3];
  products[8].colours = colourPresets[1];

  return products;
};


#endif