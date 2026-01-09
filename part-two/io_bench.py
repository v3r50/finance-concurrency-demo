import argparse
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor


def timed(label: str, fn):
    t0 = time.perf_counter()
    result = fn()
    t1 = time.perf_counter()
    dt = t1 - t0
    print(f"{label:<14}  time={dt:.3f}s")
    return dt, result


def run_single(tasks: int, delay: float) -> None:
    for _ in range(tasks):
        time.sleep(delay)


def run_threads(tasks: int, delay: float, workers: int) -> None:
    def one():
        time.sleep(delay)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(one) for _ in range(tasks)]
        for f in futures:
            f.result()


async def run_asyncio(tasks: int, delay: float) -> None:
    async def one():
        await asyncio.sleep(delay)

    await asyncio.gather(*(one() for _ in range(tasks)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tasks", type=int, default=500)
    p.add_argument("--delay_ms", type=float, default=10.0)
    p.add_argument("--workers", type=int, default=100)
    args = p.parse_args()

    delay = args.delay_ms / 1000.0

    print("I/O-bound benchmark (simulated via sleep)")
    print(f"tasks={args.tasks}, delay={args.delay_ms}ms, workers={args.workers}\n")

    dt1, _ = timed("single", lambda: run_single(args.tasks, delay))
    dt2, _ = timed("threads", lambda: run_threads(args.tasks, delay, args.workers))
    dt3, _ = timed("asyncio", lambda: asyncio.run(run_asyncio(args.tasks, delay)))

    print("\nSpeedup vs single:")
    print(f"threads x{dt1 / dt2:.2f}")
    print(f"asyncio x{dt1 / dt3:.2f}")


if __name__ == "__main__":
    main()
