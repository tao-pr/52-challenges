#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>

#include "flatbuffers/flatbuffers.h"

#include "data_generated.h"

using namespace std;
using namespace Data;

int main(int argc, char** argv)
{
  cout << "Starting ..." << endl;
  flatbuffers::FlatBufferBuilder b(5*1024); // buffer size of 5 MB
  
  // Initialise data for serialisation
  vector<flatbuffers::Offset<flatbuffers::String>> vec1 = {
    b.CreateString("Frankfurt"), b.CreateString("Köln"), b.CreateString("Amsterdam")
  };
  auto stops1 = b.CreateVector(vec1);
  auto route1 = CreateRoute(
    b, 
    stops1, 
    Status_Operating, 
    b.CreateString("DB"),
    6);


  // Serialise data into file


  // Deserialise from file


  cout << "Ending ..." << endl;
}