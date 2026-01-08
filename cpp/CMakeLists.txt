cmake_minimum_required(VERSION 3.20)
project(finance_concurrency_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

# fmt
FetchContent_Declare(
  fmt
  GIT_REPOSITORY https://github.com/fmtlib/fmt.git
  GIT_TAG 11.0.2
)
FetchContent_MakeAvailable(fmt)

# indicators (progress bar)
FetchContent_Declare(
  indicators
  GIT_REPOSITORY https://github.com/p-ranav/indicators.git
  GIT_TAG v2.3
)
FetchContent_MakeAvailable(indicators)

# CLI11
FetchContent_Declare(
  CLI11
  GIT_REPOSITORY https://github.com/CLIUtils/CLI11.git
  GIT_TAG v2.4.2
)
FetchContent_MakeAvailable(CLI11)

# Catch2
FetchContent_Declare(
  Catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v3.7.1
)
FetchContent_MakeAvailable(Catch2)

# Main executable
add_executable(finance_concurrency_cpp src/main.cpp)
target_include_directories(finance_concurrency_cpp PRIVATE include)
target_link_libraries(finance_concurrency_cpp PRIVATE fmt::fmt CLI11::CLI11 indicators)
target_compile_options(finance_concurrency_cpp PRIVATE -Wall -Wextra -Wpedantic)

# Tests
enable_testing()
add_executable(finance_concurrency_tests tests/test_invariants.cpp)
target_include_directories(finance_concurrency_tests PRIVATE include)
target_link_libraries(finance_concurrency_tests PRIVATE Catch2::Catch2WithMain fmt::fmt indicators)
target_compile_options(finance_concurrency_tests PRIVATE -Wall -Wextra -Wpedantic)

add_test(NAME finance_concurrency_tests COMMAND finance_concurrency_tests)
