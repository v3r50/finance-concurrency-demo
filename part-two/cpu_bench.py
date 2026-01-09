import argparse
import math
import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for d in range(3, r + 1, 2):
        if n % d == 0:
            return False
    return True


def count_primes_in_range(start: int, end: int) -> int:
    # CPU-bound pure Python: should NOT scale with threads in CPython (GIL)
    c = 0
    for x in range(start, end):
        if is_prime(x):
            c += 1
    return c


def chunk_ranges(start: int, end: int, chunks: int):
    total = end - start
    step = max(1, total // chunks)
    s = start
    while s < end:
        e = min(end, s + step)
        yield (s, e)
        s = e


def run_single(start: int, end: int) -> int:
    return count_primes_in_range(start, end)


def run_threads(start: int, end: int, workers: int, chunks: int) -> int:
    ranges = list(chunk_ranges(start, end, chunks))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(count_primes_in_range, s, e) for s, e in ranges]
        return sum(f.result() for f in futures)


def run_processes(start: int, end: int, workers: int, chunks: int) -> int:
    ranges = list(chunk_ranges(start, end, chunks))
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(count_primes_in_range, s, e) for s, e in ranges]
        return sum(f.result() for f in futures)


def timed(label: str, fn):
    t0 = time.perf_counter()
    result = fn()
    t1 = time.perf_counter()
    dt = t1 - t0
    print(f"{label:<14}  result={result:<8}  time={dt:.3f}s")
    return dt, result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, default=2)
    p.add_argument("--end", type=int, default=200_000)
    p.add_argument("--workers", type=int, default=os.cpu_count() or 4)
    p.add_argument("--chunks", type=int, default=0, help="0 => auto (4*workers)")
    args = p.parse_args()

    chunks = args.chunks if args.chunks > 0 else 4 * args.workers

    print("CPU-bound benchmark (prime counting, pure Python)")
    print(f"range=[{args.start}, {args.end}), workers={args.workers}, chunks={chunks}\n")

    dt1, r1 = timed("single", lambda: run_single(args.start, args.end))
    dt2, r2 = timed("threads", lambda: run_threads(args.start, args.end, args.workers, chunks))
    dt3, r3 = timed("processes", lambda: run_processes(args.start, args.end, args.workers, chunks))

    assert r1 == r2 == r3, "Mismatch in results (should be identical)"

    print("\nSpeedup vs single:")
    print(f"threads   x{dt1 / dt2:.2f}")
    print(f"processes x{dt1 / dt3:.2f}")


if __name__ == "__main__":
    main()
