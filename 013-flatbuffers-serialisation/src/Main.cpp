#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>
#include <fstream>


#include "flatbuffers/flatbuffers.h"

#include "data_generated.h"

using namespace std;
using namespace Data;

void serialise(){
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

  vector<flatbuffers::Offset<Data::Route>> routevec1 = {route1, route2};
  auto routes1  = b.CreateVector(routevec1);
  auto station1 = CreateStation(b, b.CreateString("Frankfurt"), routes1, 75);

  b.Finish(station1);
  auto size = b.GetSize();

  // Serialise data into file
  auto s = GetStation(b.GetBufferPointer());
  assert(s->title()->str() == "Frankfurt");
  assert(s->routes()->size() == 2);
  assert(s->routes()->Get(0)->operator_()->str() == "DB");
  cout << "Memory used " << size << " bytes" << endl;

  ofstream file;
  cout << "Writing to file" << endl;
  file.open("station.bin", ios::out | ios::binary);
  file.write((char*)s, size);
  file.close();
}

void deserialise(){
  // Deserialise from file
  ifstream infile("station.bin", ios::in | ios::binary);
  cout << "Reading from file back in " << endl;
  infile.seekg(0, ios::end);
  int length = infile.tellg();
  infile.seekg(0, ios::beg);
  char *data = new char[length];
  infile.read(data, length);
  infile.close();
  cout << "Memory size : " << length << " bytes" << endl;

  const Station* readStation = GetStation(data);
  cout << "Successfully deserialised" << endl;

  // Verify
  assert(readStation->title()->str() == "Frankfurt");
  assert(readStation->routes()->size() == 2);
  const flatbuffers::Vector<flatbuffers::Offset<Data::Route>>* rr = readStation->routes();
  assert(rr->Get(0)->operator_()->str() == "DB");
  assert(rr->Get(0)->stations()->size() == 4);
}

int main(int argc, char** argv){
  cout << "Starting ..." << endl;
  serialise();
  deserialise();
  cout << "Ending ..." << endl;
}