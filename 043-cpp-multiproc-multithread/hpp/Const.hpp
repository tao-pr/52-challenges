#pragma once

#include <string>

const std::string FILE_EXTENSION = ".txt";
const unsigned int NUM_PROCESSES = 3;
const unsigned int NUM_CPU_TASKS = 4;
const std::string PATH_IO_TASKS = "./data";
const float probIOBound = 0.60;

const std::string RED = "\033[31m";
const std::string BLUE = "\033[34m";
const std::string GREEN = "\033[0;32m";
const std::string MAGENTA = "\033[0;35m";
const std::string RESET = "\033[0m";
const std::string NL = "\n"; // Use this instead of std::endl to avoid flushing the buffer