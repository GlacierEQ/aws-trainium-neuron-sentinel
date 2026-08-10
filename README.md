# AWS Trainium Neuron Sentinel

**Independent local accelerator-scenario exhibit inspired by public AWS Trainium/Inferentia concepts.**

This repository is **not affiliated with, endorsed by, or operated by Amazon Web Services**. It does not establish access to AWS Neuron hardware, `neuronx-cc`, S3 Express telemetry, production Trainium/Inferentia systems, or proprietary AWS infrastructure.

## Current capability

The canonical Python surface is [`src/aws_trainium_neuron_sentinel.py`](src/aws_trainium_neuron_sentinel.py). It deterministically models:

- token partitioning across an explicit accelerator-core-count assumption;
- a simple pipeline-bubble heuristic derived from that core-count assumption;
- a latency-only throughput upper bound from an explicit latency assumption;
- SHA-256 fingerprints over the modeled result;
- fail-closed validation for invalid counts and non-finite latency assumptions.

Every modeled result emits:

`MODELED_TRAINIUM_SCENARIO_NOT_AWS_HARDWARE_MEASUREMENT`

The historical `optimize_neuron_pipeline()` method remains as a compatibility alias, but it returns the same bounded scenario model; it is not a hardware optimizer.

## Other repository surfaces

| Surface | What it proves | What it does not prove |
|---|---|---|
| `src/aws_trainium_neuron_sentinel.py` | deterministic local scenario arithmetic | AWS Neuron execution or measured performance |
| `src/neuron_allocator.cpp` | local C++ allocation/accounting reference code | Neuron persistent-memory allocation |
| `src/neuron_executor.cpp` | local arithmetic/reference C++ code | Trainium model execution |
| `src/promotion_authority.py` | local promotion/receipt authority logic | AWS deployment authority |
| `tests/` | repository-local regression and authority checks | production AWS benchmarking |

## Native proof

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
g++ -std=c++17 -Wall -Wextra -pedantic -c src/neuron_allocator.cpp -o /tmp/neuron_allocator.o
g++ -std=c++17 -Wall -Wextra -pedantic -c src/neuron_executor.cpp -o /tmp/neuron_executor.o
```

The repository truth gate runs the Python suite and compiles both C++ reference sources on the exact pull-request or push Git head. A green workflow is evidence for that exact source identity only.

## Evidence boundary

This repository does **not** claim:

- Trainium/Inferentia hardware access or execution;
- Neuron Core utilization telemetry;
- `neuronx-cc` graph compilation;
- S3 Express measurements;
- measured NPU throughput, latency, memory bandwidth, cost reduction, or model accuracy;
- multi-node/NPU collective communication;
- live MCP/APEX integration;
- AWS affiliation, endorsement, employment, production operation, or proprietary access.

## Portfolio role

The useful transferable capability is **deterministic accelerator-topology scenario modeling plus evidence-bound promotion logic**, not an assertion that this repository operates AWS infrastructure.
