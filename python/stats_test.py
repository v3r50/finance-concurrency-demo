from naive import run_once as run_naive
from locked import run_once as run_locked
from tqdm import trange
import argparse


def fmt_pln(grosze: int) -> str:
    return f"{grosze / 100:.2f} PLN"


def run_stats(fn, trials: int, label: str):
    broken = 0
    outcomes = {}

    for _ in trange(trials, desc=label):
        final = fn()
        outcomes[final] = outcomes.get(final, 0) + 1
        if final < 0:
            broken += 1

    return broken, outcomes


def print_summary(broken: int, trials: int, outcomes: dict):
    print(f"Trials: {trials}")
    print(f"Invariant broken (final < 0): {broken}")
    print(f"Broken rate: {broken / trials:.6%}")
    print("Top outcomes:")
    for val, cnt in sorted(outcomes.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {fmt_pln(val)} ({val} gr): {cnt}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=20_000)
    args = parser.parse_args()

    print("\n=== NAIVE (no lock) ===")
    broken_naive, outcomes_naive = run_stats(
        run_naive, args.trials, label="naive (no lock)"
    )
    print_summary(broken_naive, args.trials, outcomes_naive)

    print("\n=== LOCKED (with lock) ===")
    broken_locked, outcomes_locked = run_stats(
        run_locked, args.trials, label="locked"
    )
    print_summary(broken_locked, args.trials, outcomes_locked)

    # Mini-check (jak test jednostkowy)
    if broken_locked != 0:
        raise RuntimeError("ERROR: locked version broke invariant (should be 0)")

    print("\nOK: locked version never broke invariant.")


if __name__ == "__main__":
    main()
