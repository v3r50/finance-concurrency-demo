#pragma once
#include <atomic>
#include <mutex>
#include <thread>
#include "model.hpp"

// NAIVE: check-then-act bug (no UB, but logic broken)
inline i64 run_once_naive(const Params& p) {
  std::atomic<i64> balance{p.start_balance};

  auto withdraw = [&]() {
    if (balance.load(std::memory_order_relaxed) >= p.withdraw_amt) {
      balance.fetch_sub(p.withdraw_amt, std::memory_order_relaxed);
    }
  };

  std::thread t1(withdraw);
  std::thread t2(withdraw);
  t1.join();
  t2.join();

  return balance.load(std::memory_order_relaxed);
}

// LOCKED: mutex protects invariant
inline i64 run_once_locked(const Params& p) {
  i64 balance = p.start_balance;
  std::mutex m;

  auto withdraw = [&]() {
    std::lock_guard<std::mutex> lock(m);
    if (balance >= p.withdraw_amt) {
      balance -= p.withdraw_amt;
    }
  };

  std::thread t1(withdraw);
  std::thread t2(withdraw);
  t1.join();
  t2.join();

  return balance;
}
