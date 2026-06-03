# hip-benchmark-suite

A small benchmark suite for GPU compute kernels using **HIP**.

## Overview

This project is intended for exploring and comparing compute-bound kernels in a controlled way.

It currently includes:
- a CPU baseline benchmark
- a HIP kernel example
- a simple harness for repeated runs
- notes for future porting/benchmark work

## Goals

- build a small, repeatable benchmark environment
- test HIP kernels in a structured layout
- collect baseline results for later comparison
- prepare workloads that benefit from direct GPU execution

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

### CPU baseline benchmark

```bash
python scripts/bench.py --mode vector --n 2000000 --steps 3
```

### HIP example

```bash
hipcc examples/vector_add_hip.cpp -o vector_add_hip
./vector_add_hip
```

## Why HIP?

HIP gives a practical path for testing GPU compute kernels while staying close to portable C++ patterns.

This project is useful for:
- validating kernel behavior
- measuring runtime differences across environments
- preparing workloads that need direct GPU execution rather than CPU-only runs

## Notes

This repository is intentionally minimal so the benchmark flow is easy to follow.
