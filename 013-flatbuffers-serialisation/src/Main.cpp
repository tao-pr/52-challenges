#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>

#include "flatbuffers/flatbuffers.h"

#include "data.hpp"
#include "functions.hpp"

using namespace std;

int main(int argc, char** argv)
{
  cout << "Starting ..." << endl;
  auto products = generateProducts();

  assert(products.size() == 25);

  // TAOTODO




  cout << "Ending ..." << endl;
}