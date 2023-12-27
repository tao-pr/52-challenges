/**
 * CPU task
 */

#pragma once

#include <thread>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <future>
#include <algorithm>
#include <execution>
#include <random>

// https://github.com/oneapi-src/oneTBB/blob/master/examples/parallel_for_each/parallel_preorder/parallel_preorder.cpp
#include "oneapi/tbb/parallel_for_each.h"

#include "Const.hpp"

class CPUTask
{
public:

  // Follow the signature from the OneTBB example usage of `parallel_for_each`
  void operator()(int n, oneapi::tbb::feeder<int> &feeder) const
  {
    std::cout << "CPU task computing element: " << n << std::endl;
    // taotodo
  };
};

/**
 * Generate N coroutines
 */
void runTasks(std::mt19937 &gen, int pid, int num)
{
  std::vector<std::thread> threads;
  std::vector<std::future<int>> futures;

  // Randomly generating M inputs
  auto unif = std::uniform_int_distribution<>(0, 10);
  std::vector<int> data{};
  std::ostringstream vecStr;
  for (int n = 0; n < num; n++)
  {
    auto d = unif(gen);
    data.push_back(d);
    vecStr << d << ", ";
  }
  std::cout << "[PID " << pid << " ] CPU task generated data: " << vecStr.str() << std::endl;

  // `parallel_for_each` expects constant iterator
  oneapi::tbb::parallel_for_each(
      data.cbegin(),
      data.cend(),
      CPUTask());

  // taotodo how to wait for all results?
}