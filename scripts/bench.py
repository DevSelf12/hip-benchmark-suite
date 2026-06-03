#!/usr/bin/env python3
import argparse
import time


def vector_bench(n: int, steps: int):
    a = [1.0] * n
    b = [2.0] * n
    c = [0.0] * n

    times = []
    for _ in range(steps):
        t0 = time.perf_counter()
        for i in range(n):
            c[i] = a[i] + b[i]
        dt = time.perf_counter() - t0
        times.append(dt)

    avg = sum(times) / len(times)
    return {
        "mode": "vector",
        "n": n,
        "steps": steps,
        "avg_sec": round(avg, 6),
        "times": [round(t, 6) for t in times],
    }


def main():
    parser = argparse.ArgumentParser(description="hip-benchmark-suite bench")
    parser.add_argument("--mode", default="vector", choices=["vector"])
    parser.add_argument("--n", type=int, default=1000000)
    parser.add_argument("--steps", type=int, default=3)
    args = parser.parse_args()

    if args.mode == "vector":
        result = vector_bench(args.n, args.steps)

    print("[bench] result:")
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
