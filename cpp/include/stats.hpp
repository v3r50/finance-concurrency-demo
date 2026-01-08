#pragma once
#include <unordered_map>
#include <vector>
#include <algorithm>

#include <fmt/core.h>
#include <indicators/progress_bar.hpp>
#include <indicators/cursor_control.hpp>

#include "model.hpp"

struct Stats {
  std::size_t trials = 0;
  std::size_t broken = 0;
  std::unordered_map<i64, std::size_t> outcomes;
};

template <typename Fn>
inline Stats run_stats(Fn fn, std::size_t trials, const std::string& label) {
  using namespace indicators;

  show_console_cursor(false);
  ProgressBar bar{
    option::PrefixText{label},
    option::BarWidth{45},
    option::ShowElapsedTime{true},
    option::ShowRemainingTime{true}
  };

  Stats s{};
  s.trials = trials;

  for (std::size_t i = 1; i <= trials; ++i) {
    i64 final = fn();
    s.outcomes[final]++;
    if (!invariant_ok(final)) s.broken++;
    bar.set_progress(static_cast<int>((i * 100) / trials));
  }

  bar.set_progress(100);
  show_console_cursor(true);
  fmt::print("\n");
  return s;
}

inline void print_summary(const Stats& s) {
  fmt::print("Trials: {}\n", s.trials);
  fmt::print("Invariant broken: {}\n", s.broken);
  fmt::print("Broken rate: {:.6f}%\n",
             s.trials ? (100.0 * s.broken / s.trials) : 0.0);

  std::vector<std::pair<i64, std::size_t>> v(s.outcomes.begin(), s.outcomes.end());
  std::sort(v.begin(), v.end(), [](auto& a, auto& b){ return a.second > b.second; });

  fmt::print("Top outcomes:\n");
  for (std::size_t i = 0; i < std::min<std::size_t>(5, v.size()); ++i) {
    fmt::print("  {} : {}\n", pln(v[i].first), v[i].second);
  }
}
