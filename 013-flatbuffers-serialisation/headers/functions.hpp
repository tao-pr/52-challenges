#ifndef FUNC_HPP
#define FUNC_HPP

#include <vector>

#include "data.hpp"

using namespace std;

inline vector<Campaign> generateCampaigns(int numCampaigns){
  auto camps = vector<Campaign>();
  if (numCampaigns <= 1) camps.push_back(Campaign(5, "30% Off"));
  if (numCampaigns <= 2) camps.push_back(Campaign(14, "10% Off"));
  if (numCampaigns <= 3) camps.push_back(Campaign(10, "Buy one get one FREE"));
  if (numCampaigns <= 4) camps.push_back(Campaign(5, "Buy 2 get one FREE"));
  if (numCampaigns <= 5) camps.push_back(Campaign(10, "Summer SALE"));
  return camps;
};

inline vector<Product> generateProducts(){
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

  products[0].campaigns = generateCampaigns(1);
  products[1].campaigns = generateCampaigns(4);
  products[2].campaigns = generateCampaigns(4);
  products[3].campaigns = generateCampaigns(3);
  products[4].campaigns = generateCampaigns(1);
  products[5].campaigns = generateCampaigns(2);
  products[6].campaigns = generateCampaigns(2);
  products[7].campaigns = generateCampaigns(3);
  products[8].campaigns = generateCampaigns(5);

  return products;
};


#endif