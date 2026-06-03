# Design

## Purpose

This repository is structured as a lightweight benchmark lab.

## Principles

- keep the layout simple
- separate examples, docs, and benchmarks
- make runs easy to reproduce
- favor small, focused kernels

## Benchmark workflow

1. run baseline benchmark
2. record runtime metrics
3. compare with GPU/HIP execution later
4. store notes in `benchmarks/`

## Future direction

The next step is to move from CPU-only baselines into HIP kernels that can be validated on a real GPU environment.
