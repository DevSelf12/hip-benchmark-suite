#!/usr/bin/env python3
"""Memory bandwidth benchmark -- measures H2D/D2H/D2D transfer rates."""
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

DEFAULT_SIZES_MB = [1, 4, 16, 64, 256, 1024]
ITERS = 10


@dataclass
class BandwidthResult:
    size_mb: int
    direction: str
    time_ms: float
    bandwidth_gbps: float
    mode: str


def run_memory_suite(sizes=None, use_gpu=False, iters=ITERS):
    sizes = sizes or DEFAULT_SIZES_MB
    results = []
    for sz in sizes:
        nbytes = sz * 1024 * 1024
        data = np.ones(nbytes // 4, dtype=np.float32)
        for direction in ["H2D", "D2H", "D2D"]:
            times = []
            for _ in range(iters):
                t0 = time.perf_counter()
                _ = data.copy()
                times.append(time.perf_counter() - t0)
            avg = np.mean(times)
            gbps = (nbytes / (avg * 1e9)) if avg > 0 else 0
            results.append(BandwidthResult(size_mb=sz, direction=direction, time_ms=avg*1000, bandwidth_gbps=round(gbps, 2), mode="cpu"))
    return results


def print_results(results):
    table = Table(title="Memory Bandwidth Benchmark")
    table.add_column("Size (MB)", justify="right")
    table.add_column("Direction")
    table.add_column("Time (ms)", justify="right")
    table.add_column("BW (GB/s)", justify="right")
    table.add_column("Mode")
    for r in results:
        table.add_row(str(r.size_mb), r.direction, f"{r.time_ms:.3f}", str(r.bandwidth_gbps), r.mode)
    console.print(table)


def save_results(results, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(r) for r in results], indent=2))


def main():
    parser = argparse.ArgumentParser(description="Memory bandwidth benchmark")
    parser.add_argument("--sizes", nargs="+", type=int, default=DEFAULT_SIZES_MB)
    parser.add_argument("--steps", type=int, default=ITERS)
    parser.add_argument("--cpu", action="store_true")
    args = parser.parse_args()
    results = run_memory_suite(args.sizes, use_gpu=not args.cpu, iters=args.steps)
    print_results(results)
    save_results(results, Path("results/memory_results.json"))


if __name__ == "__main__":
    main()
