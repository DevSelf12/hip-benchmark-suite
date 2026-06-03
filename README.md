# hip-benchmark-suite

A structured benchmark suite for HIP compute kernel experiments.

## Overview

This repository is designed for small, repeatable GPU compute experiments.

It focuses on:
- CPU baseline benchmarking
- HIP kernel execution
- simple runtime comparison workflows
- clean experiment documentation

The intent is to build a lightweight environment for validating numerical kernels and preparing GPU-oriented workloads.

## Key features

- minimal benchmark harness
- HIP kernel example
- reproducible CPU baseline
- structured benchmark notes
- simple repository layout for technical review

## Repository layout

```
hip-benchmark-suite/
├── README.md
├── LICENSE
├── .gitignore
├── benchmarks/
│   └── results.md
├── docs/
│   ├── design.md
│   └── notes.md
├── examples/
│   └── vector_add_hip.cpp
└── scripts/
    ├── run_all.sh
    └── bench.py
```

## Quick start

### Run CPU baseline benchmark

```bash
python scripts/bench.py --mode vector --n 2000000 --steps 3
```

### Build and run HIP example

```bash
hipcc examples/vector_add_hip.cpp -o vector_add_hip
./vector_add_hip
```

## Benchmark workflow

1. run baseline benchmark
2. record runtime metrics
3. compare execution paths later
4. document findings in `benchmarks/`

## Why this project exists

This repository exists to support a simple but clear experimentation workflow around HIP-based compute workloads.

## License

MIT
