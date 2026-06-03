# hip-benchmark-suite

[![HIP](https://img.shields.io/badge/HIP-kernel%20benchmarks-ED1C24?logo=amd&logoColor=white)](https://rocm.docs.amd.com/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/DevSelf12/hip-benchmark-suite/actions/workflows/lint.yml/badge.svg)](https://github.com/DevSelf12/hip-benchmark-suite/actions)

**Structured benchmark suite for HIP compute kernel experiments — vector math, dot products, matrix multiplication, and memory bandwidth on AMD GPUs.**

Designed for repeatable performance characterization and kernel validation on ROCm environments.

---

## Architecture

```
+--------------------------------------------------------------+
|                        run_all.py                             |
|                   (orchestrator + CLI)                         |
+----------+----------+---------------+-------------------------+
|  Vector  | Dot      | Matrix        | Memory Bandwidth        |
|  Add     | Product  | Multiply      | hipMemcpy H2D/D2H       |
|  FP32    | FP32     | FP16/FP32     | GB/s measurement        |
+----------+----------+---------------+-------------------------+
|                      utils/                                    |
|  gpu_monitor.py (ROCm SMI)  |  report_generator.py            |
|  live temp/power/VRAM       |  markdown + matplotlib charts    |
+--------------------------------------------------------------+
```

## Features

| Benchmark | What it measures | Key metrics |
|:---|:---|:---|
| **Vector Add** | Element-wise vector addition | Throughput (GB/s), latency |
| **Dot Product** | Reduction kernel performance | TFLOPS, bandwidth utilization |
| **Matrix Multiply** | GEMM via HIP | TFLOPS, GFLOPS |
| **Memory Bandwidth** | PCIe/xGMI transfer rates | H2D, D2H, D2D (GB/s) |
| **GPU Monitor** | Real-time hardware state | Temp, power, VRAM, utilization |

### Supported Hardware

| GPU | VRAM | Architecture | Status |
|:---|---:|:---|:---:|
| AMD Instinct MI300X | 192 GB HBM3 | CDNA 3 | Primary |
| AMD Instinct MI250X | 128 GB HBM2e | CDNA 2 | Tested |
| AMD Instinct MI210 | 64 GB HBM2e | CDNA 2 | Tested |

---

## Quick Start

### Prerequisites

- AMD GPU with ROCm 6.x installed ([install guide](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/))
- Python 3.10+
- HIP compiler (hipcc)

### Install

```bash
git clone https://github.com/DevSelf12/hip-benchmark-suite.git
cd hip-benchmark-suite
pip install -r requirements.txt
```

### Run All Benchmarks

```bash
python run_all.py
python run_all.py --suite vector dot
python run_all.py --cpu
```

### Individual Benchmarks

```bash
python -m benchmarks.vector_add --n 2000000 --steps 5
python -m benchmarks.dot_product --n 2000000
python -m benchmarks.matrix_mul --sizes 512 1024 2048
python -m benchmarks.memory_bandwidth
```

### Build HIP Examples

```bash
hipcc examples/vector_add_hip.cpp -o vector_add_hip && ./vector_add_hip
hipcc examples/dot_product_hip.cpp -o dot_product_hip && ./dot_product_hip
hipcc examples/matrix_mul_hip.cpp -o matrix_mul_hip && ./matrix_mul_hip
```

---

## Output

All benchmarks produce structured JSON in `results/`:

```
results/
+-- vector_results.json
+-- dot_results.json
+-- matrix_results.json
+-- memory_results.json
+-- BENCHMARK_REPORT.md
+-- performance.png
```

---

## Project Structure

```
hip-benchmark-suite/
+-- benchmarks/
|   +-- __init__.py
|   +-- vector_add.py          # Vector addition benchmark
|   +-- dot_product.py         # Dot product reduction benchmark
|   +-- matrix_mul.py          # Matrix multiplication benchmark
|   +-- memory_bandwidth.py    # Memory transfer benchmark
+-- examples/
|   +-- vector_add_hip.cpp     # HIP vector add kernel
|   +-- dot_product_hip.cpp    # HIP dot product kernel
|   +-- matrix_mul_hip.cpp     # HIP matrix multiply kernel
+-- utils/
|   +-- __init__.py
|   +-- gpu_monitor.py         # ROCm SMI wrapper
|   +-- report_generator.py    # Markdown + chart generation
+-- results/                   # Benchmark output (JSON + charts)
+-- .github/workflows/         # CI: lint + type check
+-- run_all.py                 # Main entry point
+-- Dockerfile                 # ROCm container
+-- requirements.txt
+-- pyproject.toml
+-- LICENSE
```

---

## Development

```bash
pip install -e ".[dev]"
ruff check .
mypy benchmarks/ utils/ run_all.py
python run_all.py --cpu
```

The `--cpu` flag enables development on any machine. All code paths are exercised except actual HIP kernel calls.

---

## Roadmap

- [ ] ROCm profiler integration (rocprof v2)
- [ ] Multi-GPU benchmark scaling
- [ ] Power efficiency metrics (TFLOPS/watt)
- [ ] Cross-vendor comparison support
- [ ] Flash Attention 2 benchmark (Composable Kernel)

---

## Citation

If you use hip-benchmark-suite in your research, please cite:

```bibtex
@software{hip_benchmark_suite_2026,
  title  = {hip-benchmark-suite: HIP Kernel Benchmarks for AMD GPUs},
  author = {DevSelf12},
  year   = {2026},
  url    = {https://github.com/DevSelf12/hip-benchmark-suite},
}
```

---

## Acknowledgments

- [AMD ROCm](https://www.amd.com/en/products/software/rocm.html) -- open-source GPU computing platform
- [hipBLAS](https://github.com/ROCmSoftwarePlatform/hipBLAS) -- GPU-accelerated BLAS
- AMD Developer Cloud for GPU access during development

---

## License

MIT -- see [LICENSE](LICENSE).
