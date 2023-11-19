/**
 * Define classes
 *
 */

#pragma once

#include <variant>
#include <vector>
#include <mutex>
#include <ctime>

// Thread-safe shareable data
struct Shareable
{
  std::time_t ts; // timestamp
  std::vector<int> data;
  int fromPid;

  Shareable(std::vector<int> data, int fromPid) : data(data), fromPid(fromPid), ts(std::time(nullptr)) {}

  // Thread-safely add an element to [data]
  void add(const int d, std::mutex& m)
  {
    const std::lock_guard<std::mutex> lock(m);
    data.push_back(d);
  }
};

/**
 * A variant which can be either empty (monostate), Shareable or an error message (string)
 */
using ShareableVariant = std::variant<std::monostate, Shareable, std::string>;

/**
 * Print value of ShareableVariant (without Newline)
 * Wrapped in Function-try-block
 */
void printVariant(const ShareableVariant &sv)
try
{
  using namespace std;
  if (std::holds_alternative<std::monostate>(sv))
  {
    // Empty
    cout << "(empty)";
  }
  else if (std::holds_alternative<Shareable>(sv))
  {
    // Shareable
    Shareable s = std::get<Shareable>(sv);
    auto strTimestamp = std::asctime(std::localtime(&s.ts));
    
    // Print all elements in [data]
    cout << "[PID: " << s.fromPid << "] data (";
    for (const auto& v : s.data) 
      cout << v << ", ";
    cout << ") @" << strTimestamp;
  }
  else if (std::holds_alternative<std::string>(sv))
  {
    // Error
    cout << "ERR data (" << std::get<std::string>(sv) << ")";
  }
}
catch (...)
{
  std::cout << RED << "Unable to parse shareable data" << std::endl;
  throw;
}
