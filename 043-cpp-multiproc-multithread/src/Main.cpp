#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <random>

// Params / Consts
const unsigned int NUM_PROCESSES = 5;
const float probIOBound = 0.25;

const std::string RED = "\033[31m";
const std::string BLUE = "\033[34m";
const std::string RESET = "\033[0m";
const std::string NL = "\n"; // Use this instead of std::endl to avoid flushing the buffer

int runIOBoundTask()
{
  // taotodo
  std::cout << "[PID: " << getpid() << "] Running IO bounded task" << NL;
}

int runCPUBoundTask()
{
  // taotodo
  std::cout << "PID: " << getpid() << "] Running CPU bounded task" << NL;
}

/**
 * Fork create a new process (UNIX)
 * returns error code
 */
int forkProcess(int i)
{
  pid_t pid = fork();

  if (pid < 0)
  {
    // Error occurred
    std::cerr << RED << "Fork failed" << RESET << NL;
    return -1;
  }
  else if (pid == 0)
  {
    // This block is executed by the child process
    std::cout << BLUE << "Forked process: " << RESET << "Child process created. PID: " << getpid() << NL;

    // Run multiple threads
    if (std::rand() < probIOBound)
    {
      // Run IO bounded task
      runIOBoundTask();
    }
    else
    {
      // Run CPU bounded task
      runCPUBoundTask();
    }

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
    wait(NULL);
  }

  std::cout << "Master process exiting." << std::endl;
  return 0;
}