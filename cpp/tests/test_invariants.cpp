#include <catch2/catch_test_macros.hpp>
#include "model.hpp"
#include "scenarios.hpp"

TEST_CASE("locked never breaks invariant") {
  Params p{};
  for (int i = 0; i < 20000; ++i) {
    REQUIRE(invariant_ok(run_once_locked(p)));
  }
}

TEST_CASE("naive can break invariant (probabilistic)") {
  Params p{};
  bool seen = false;

  for (int i = 0; i < 20000; ++i) {
    if (!invariant_ok(run_once_naive(p))) {
      seen = true;
      break;
    }
  }

  if (!seen) {
    WARN("naive version did NOT break invariant in this run (probabilistic)");
  }
}
