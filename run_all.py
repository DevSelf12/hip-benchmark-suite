#!/usr/bin/env python3
"""Main entry point -- run all hip-benchmark-suite benchmarks and generate report."""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="hip-benchmark-suite -- HIP kernel benchmarks for AMD GPUs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python run_all.py                     # Run all benchmarks
  python run_all.py --suite vector dot  # Run specific suites
  python run_all.py --cpu               # Force CPU simulation mode
        """,
    )
    parser.add_argument("--suite", nargs="+",
                        choices=["vector", "dot", "matrix", "memory", "all"],
                        default=["all"])
    parser.add_argument("--cpu", action="store_true")
    parser.add_argument("--output", "-o", default="results")
    parser.add_argument("--iters", type=int, default=10)
    args = parser.parse_args()

    suites = args.suite if "all" not in args.suite else ["vector", "dot", "matrix", "memory"]
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    console.print(Panel.fit(
        f"[bold white]hip-benchmark-suite[/bold white]\n"
        f"Suites: {', '.join(suites)}\n"
        f"Mode: {'CPU simulation' if args.cpu else 'GPU (ROCm/HIP)'}",
        title="[red]AMD[/red] HIP Benchmarks",
        border_style="red",
    ))

    t_start = time.time()

    if "vector" in suites:
        console.print("\n[bold]=== Vector Add ===[/bold]")
        from benchmarks.vector_add import run_vector_suite, print_results, save_results
        r = run_vector_suite(use_gpu=not args.cpu, iters=args.iters)
        print_results(r)
        save_results(r, output / "vector_results.json")

    if "dot" in suites:
        console.print("\n[bold]=== Dot Product ===[/bold]")
        from benchmarks.dot_product import run_dot_suite, print_results as pr, save_results as sr
        r = run_dot_suite(use_gpu=not args.cpu, iters=args.iters)
        pr(r)
        sr(r, output / "dot_results.json")

    if "matrix" in suites:
        console.print("\n[bold]=== Matrix Multiply ===[/bold]")
        from benchmarks.matrix_mul import run_matrix_suite, print_results as mp, save_results as ms
        r = run_matrix_suite(use_gpu=not args.cpu, iters=args.iters)
        mp(r)
        ms(r, output / "matrix_results.json")

    if "memory" in suites:
        console.print("\n[bold]=== Memory Bandwidth ===[/bold]")
        from benchmarks.memory_bandwidth import run_memory_suite, print_results as lp, save_results as ls
        r = run_memory_suite(use_gpu=not args.cpu, iters=args.iters)
        lp(r)
        ls(r, output / "memory_results.json")

    console.print(f"\n[green]Done in {time.time() - t_start:.1f}s[/green]")
    from utils.report_generator import generate_report
    generate_report(output)


if __name__ == "__main__":
    main()
