/**
 * IO Task
 */

#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <variant>
#include <filesystem>
#include <future>
#include <fstream>
#include <thread>

#include "Const.hpp"

// Variant of file content, can be empty
using ContentVariant = std::variant<std::monostate, std::vector<std::string>>;

ContentVariant readFile(const int pid, const std::string &path, bool verbose)
try
{
  auto tid = std::this_thread::get_id();
  if (verbose)
    std::cout << "[PID:" << pid << " | ThreadID : " << tid << "] Reading file: " << path << std::endl;
  std::ifstream file(path);
  std::vector<std::string> lines;

  // Read lines
  for (std::string ln; std::getline(file, ln);)
    lines.push_back(ln);

  std::cout << "[PID:" << pid << " | ThreadID : " << tid << "] Done reading" << std::endl;
  return lines;
}
catch (...)
{
  std::cout << RED << "[PID:" << pid << "] Unable to read file " << path << RESET << std::endl;
  return std::monostate{};
}

std::vector<std::future<ContentVariant>> readFiles(int pid, const std::string dir, bool verbose)
{
  std::vector<std::future<ContentVariant>> futures;
  for (auto &file : std::filesystem::directory_iterator(dir))
  {
    if (file.is_regular_file() && file.path().extension() == FILE_EXTENSION)
    {
      // Launch a new thread (IO bound)
      std::future<ContentVariant> future = std::async(std::launch::async, readFile, pid, file.path(), verbose);
      futures.push_back(std::move(future));
    }
  }
  return std::move(futures);
}