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

#include "Const.hpp"

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

  std::cout << "[PID: " << pid << "] generating " << num << " tasks: " << vecStr.str() << std::endl;

  // Now run M parallel tasks on the vector
  std::for_each(
      std::execution::par,
      data.begin(),
      data.end(),
      [](int &n)
      {
        std::cout << "CPU task computing element: " << n << std::endl;
        // taotodo
      });
}