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

struct TaskInfo
{
  int pid;
  int n;
};

class CPUTask
{
public:
  // Follow the signature from the OneTBB example usage of `parallel_for_each`
  void operator()(TaskInfo ti, oneapi::tbb::feeder<TaskInfo> &feeder) const
  {
    std::cout << MAGENTA << "[PID " << ti.pid << " ]" << RESET << " CPU task computing #" << ti.n << std::endl;

    // count from 1 to n*10^6
    unsigned int sum{};
    for (auto i = 1; i < ti.n * 1000000; i++)
    {
      sum += i;
    }

    std::cout << MAGENTA << "[PID " << ti.pid << " ]" << GREEN << " CPU task DONE #" << ti.n << RESET << std::endl;
  };
};

/**
 * Generate N coroutines
 */
void runTasks(std::mt19937 &gen, int pid, int num)
{
  std::vector<std::thread> threads;
  std::vector<std::future<TaskInfo>> futures;

  // Randomly generating M inputs
  auto unif = std::uniform_int_distribution<>(0, 10);
  std::vector<TaskInfo> data{};

  for (int n = 0; n < num; n++)
  {
    auto d = unif(gen);
    data.push_back(TaskInfo{pid, d});
  }

  // More about `tbb::parallel_for_each`
  // https://spec.oneapi.io/versions/latest/elements/oneTBB/source/algorithms/functions/parallel_for_each_func.html

  // `parallel_for_each` expects constant iterator
  oneapi::tbb::parallel_for_each(
      data.cbegin(),
      data.cend(),
      CPUTask());

  std::cout << MAGENTA << "[PID " << pid << " ] " << GREEN << "All " << NUM_CPU_TASKS  << " CPU tasks are done." << RESET << NL;
}