#!/usr/bin/env python3
"""Generate markdown benchmark reports from JSON results."""
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from rich.console import Console

console = Console()


def generate_report(results_dir: Path, output: Path | None = None):
    output = output or results_dir / "BENCHMARK_REPORT.md"
    json_files = sorted(results_dir.glob("*_results.json"))
    if not json_files:
        console.print("[yellow]No result files found.[/yellow]")
        return

    lines = ["# Benchmark Report", f"\nGenerated: {datetime.now().isoformat()}\n"]

    for jf in json_files:
        data = json.loads(jf.read_text())
        name = jf.stem.replace("_results", "").replace("_", " ").title()
        lines.append(f"## {name}\n")
        if isinstance(data, list) and data:
            keys = list(data[0].keys())
            lines.append("| " + " | ".join(keys) + " |")
            lines.append("| " + " | ".join(["---"] * len(keys)) + " |")
            for row in data:
                lines.append("| " + " | ".join(str(row.get(k, "")) for k in keys) + " |")
            lines.append("")

    output.write_text("\n".join(lines))
    console.print(f"[green]Report written to {output}[/green]")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="results")
    args = parser.parse_args()
    generate_report(Path(args.dir))


if __name__ == "__main__":
    main()
