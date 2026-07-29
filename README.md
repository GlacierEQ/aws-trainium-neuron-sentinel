# AWS Trainium Neuron Sentinel — AWS NPU Acceleration Sentinel ☁️

> **Performance monitor and compiler sentinel for AWS Trainium (Trn1) and Inferentia (Inf2) Neuron NPUs.**

[![C++](https://img.shields.io/badge/C++-17-00599C)]()
[![Python](https://img.shields.io/badge/Python-3.9+-blue)]()
[![Domain](https://img.shields.io/badge/Domain-AWS%20Neuron%20NPU-orange)]()

---

## 🎯 For Recruiters & Hiring Managers

This repository implements a **sentinel and compiler optimization suite for AWS Trainium & Inferentia** — maximizing throughput on AWS custom AI chips. It demonstrates:

- **Neuron Core utilization profiling** tracking execution latency and memory bandwidth
- **C++ memory allocator optimization** for Neuron persistent memory
- **Graph compilation tuning** for AWS Neuron Compiler (`neuronx-cc`)
- **Multi-NPU collective communication** monitoring across Trn1 architecture

**Why this matters**: As cloud providers deploy custom AI accelerators (Trainium, Inferentia), engineering teams must optimize software specifically for non-NVIDIA silicon to reduce cloud compute costs by 50%+.

---

## 🔬 For Engineers & Technical Reviewers

### Core Components

| Component | Language | Purpose |
|---|---|---|
| `src/neuron_sentinel.cpp` | C++ | Low-overhead C++ Neuron Core execution profiler |
| `src/neuron_monitor.py` | Python | High-level compiler wrapper and telemetry aggregator |
| `tests/` | Python | NPU throughput and latency benchmarks |

---

## 🤖 ML/AI & Programmatic Mesh Integration

- **MCP Tool**: `aws_npu_health()` — NPU telemetry queryable by swarm agents
- **Mastermind Sidecar**: Connected to APEX Highway mesh
- **SHA-256 Integrity**: Tracked in `.integrity/file_hashes.json`

---

## ⚡ Quick Start

```bash
python3 src/neuron_monitor.py
python3 tests/test_neuron.py
```
