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
    b.CreateString("Frankfurt"), b.CreateString("Köln"), b.CreateString("Düsseldorf"), b.CreateString("Amsterdam")
  };
  auto stops1 = b.CreateVector(vec1);
  auto route1 = CreateRoute(
    b, 
    stops1, 
    Status_Operating, 
    b.CreateString("DB"),
    6);

  vector<flatbuffers::Offset<flatbuffers::String>> vec2 = {
    b.CreateString("Frankfurt"), b.CreateString("Ingolstadt"), b.CreateString("München")
  };
  auto stops2 = b.CreateVector(vec2);
  auto route2 = CreateRoute(
    b, 
    stops2, 
    Status_Operating, 
    b.CreateString("DB"),
    5);

  vector<flatbuffers::Offset<flatbuffers::String>> vec3 = {
    b.CreateString("Amsterdam"), b.CreateString("Rotterdam")
  };
  auto stops3 = b.CreateVector(vec3);
  auto route3 = CreateRoute(
    b, 
    stops3, 
    Status_Operating, 
    b.CreateString("NS"),
    40);

  // Serialise data into file


  // Deserialise from file


  cout << "Ending ..." << endl;
}