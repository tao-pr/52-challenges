#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <random>
#include <unordered_map>
#include <variant>

#include "Const.hpp"
#include "Shareable.hpp" // Variants for sharable data type
#include "IO.hpp"        // File reader
#include "CPU.hpp"      // Cpu bound task

int runIOBoundTask()
{
  std::cout << "[PID: " << getpid() << "] Running IO bounded task" << NL;

  // Load files from the dir
  // Number of threads = number of .txt files

  const bool verbose = true;
  auto futures = readFiles(getpid(), PATH_IO_TASKS, verbose);

  int nFinished{};
  for (auto &f : futures)
  {
    // In fact, this following block waits and blocks CPU time
    // until it receives the result from each future sequentially.
    auto v = f.get();
    if (std::holds_alternative<std::vector<std::string>>(v))
    {
      std::cout << "[PID: " << getpid() << "] " << GREEN << "read file completed" << RESET << NL;
      for (const auto &ln : std::get<std::vector<std::string>>(v))
      {
        std::cout << "   " << ln << NL;
      }
      nFinished++;
    }
  }

  std::cout << "[PID: " << getpid() << " ] " << GREEN << nFinished << " IO threads finished" << std::endl;

  return nFinished;
}

int runCPUBoundTask(std::mt19937& gen)
{
  std::cout << MAGENTA << "[PID: " << getpid() << "] " << RESET << "Running CPU bounded task" << NL;

  // Create N subtasks
  runTasks(gen, getpid(), NUM_CPU_TASKS);
}

/**
 * Fork create a new process (UNIX)
 * returns error code
 */
int forkProcess(int i)
{
  pid_t pid = fork();

  // NOTE: In multi-process app, each process must have its own random generator

  // https://en.cppreference.com/w/cpp/numeric/random/uniform_real_distribution
  std::random_device rd;  // Will be used to obtain a seed for the random number engine
  std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()

  if (pid < 0)
  {
    // Error occurred
    std::cerr << RED << "Fork failed" << RESET << NL;
    return -1;
  }
  else if (pid == 0)
  {
    // This block is executed by the child process
    std::cout << "Forked process: " << "Child process created. PID: " << getpid() << NL;

    // Run multiple threads
    auto unif = std::uniform_real_distribution<>(0.0, 1.0);
    if (unif(gen) < probIOBound)
    {
      // Run IO bounded tasks (num threads = num files to read)
      runIOBoundTask();
    }
    else
    {
      // Run CPU bounded tasks
      runCPUBoundTask(gen);
    }

    std::cout << "[PID " << getpid() << "] exiting" << NL;
    _exit(0); // Child process exits
  }
  else
  {
    // This block is executed by the parent process
    std::cout << "[Parent process] Created a child with PID: " << pid << std::endl;
    return 0;
  }
}

int main()
{
  std::srand(std::time(nullptr));

  for (int i = 0; i < NUM_PROCESSES; ++i)
  {
    forkProcess(i);
  }

  // Parent waits for all child processes to finish
  for (int i = 0; i < NUM_PROCESSES; ++i)
  {
    std::cout << "Waiting for process: " << i << std::endl;
    wait(NULL);
  }

  std::cout << "Master process exiting." << std::endl;
  return 0;
}