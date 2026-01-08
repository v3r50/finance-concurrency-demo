#pragma once
#include <cstdint>
#include <string>
#include <fmt/format.h>

using i64 = std::int64_t;

struct Params {
  i64 start_balance = 100'000; // grosze
  i64 withdraw_amt  = 70'000;  // grosze
};

inline bool invariant_ok(i64 balance) {
  return balance >= 0;
}

inline std::string pln(i64 grosze) {
  return fmt::format("{:.2f} PLN", grosze / 100.0);
}
