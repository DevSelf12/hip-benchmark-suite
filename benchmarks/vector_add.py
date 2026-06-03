#!/usr/bin/env python3
"""Vector addition benchmark -- measures element-wise throughput."""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_N = [100000, 500000, 1000000, 2000000, 5000000]
ITERS = 10


@dataclass
class VectorResult:
    n: int
    time_ms: float
    throughput_gbps: float
    mode: str


def run_vector_suite(n_values=None, use_gpu=False, iters=ITERS):
    n_values = n_values or DEFAULT_N
    results = []
    for n in n_values:
        a = np.ones(n, dtype=np.float32)
        b = np.ones(n, dtype=np.float32)
        for _ in range(3):
            _ = a + b
        times = []
        for _ in range(iters):
            t0 = time.perf_counter()
            c = a + b
            times.append(time.perf_counter() - t0)
        avg = np.mean(times)
        gbps = (n * 4 * 3) / (avg * 1e9)
        results.append(VectorResult(n=n, time_ms=avg * 1000, throughput_gbps=round(gbps, 2), mode="cpu"))
    return results


def print_results(results):
    table = Table(title="Vector Add Benchmark")
    table.add_column("N", justify="right")
    table.add_column("Time (ms)", justify="right")
    table.add_column("Throughput (GB/s)", justify="right")
    table.add_column("Mode")
    for r in results:
        table.add_row(str(r.n), f"{r.time_ms:.3f}", str(r.throughput_gbps), r.mode)
    console.print(table)


def save_results(results, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(r) for r in results], indent=2))


def main():
    parser = argparse.ArgumentParser(description="Vector add benchmark")
    parser.add_argument("--n", nargs="+", type=int, default=DEFAULT_N)
    parser.add_argument("--steps", type=int, default=ITERS)
    parser.add_argument("--cpu", action="store_true")
    args = parser.parse_args()
    results = run_vector_suite(args.n, use_gpu=not args.cpu, iters=args.steps)
    print_results(results)
    save_results(results, Path("results/vector_results.json"))


if __name__ == "__main__":
    main()
