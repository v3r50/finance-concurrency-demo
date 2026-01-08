#include <CLI/CLI.hpp>
#include <fmt/core.h>

#include "model.hpp"
#include "scenarios.hpp"
#include "stats.hpp"

int main(int argc, char** argv) {
  std::size_t trials = 10'000;
  std::string mode = "both";

  Params p{};

  CLI::App app{"Concurrency invariant demo (C++)"};
  app.add_option("--trials", trials)->check(CLI::PositiveNumber);
  app.add_option("--mode", mode)->check(CLI::IsMember({"naive","locked","both"}));

  CLI11_PARSE(app, argc, argv);

  if (mode == "naive" || mode == "both") {
    fmt::print("=== NAIVE ===\n");
    auto s = run_stats([&]{ return run_once_naive(p); }, trials, "naive");
    print_summary(s);
    fmt::print("\n");
  }

  if (mode == "locked" || mode == "both") {
    fmt::print("=== LOCKED ===\n");
    auto s = run_stats([&]{ return run_once_locked(p); }, trials, "locked");
    print_summary(s);

    if (s.broken != 0) {
      fmt::print("ERROR: locked version broke invariant\n");
      return 1;
    }
  }

  return 0;
}
