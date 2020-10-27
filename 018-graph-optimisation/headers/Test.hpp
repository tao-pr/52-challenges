#pragma once

#include <memory>
#include <vector>
#include <stack>
#include <map>
#include <string>
#include <iostream>
#include <fmt/format.h>

#include "Base.hpp"

using namespace std;

class TestCase {
public:
  string title;
  bool test() const;
};

class TestSuite {

public:
  inline bool testAll(vector<TestCase>& cases) const {
    bool aggRes = true;
    for (auto& c : cases){
      auto v = c.test();
      auto res = v ? "[PASSED]" : "[FAILED]";
      auto str = fmt::format("Running test case : {} ... {}", c.title, res);
      aggRes &= v;
    }
    return aggRes;
  };

};

