#!/usr/bin/env python3
"""Cold-start: AWSTrainiumNeuronSentinel pipeline optimize path."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from aws_trainium_neuron_sentinel import AWSTrainiumNeuronSentinel

def main() -> int:
    res = AWSTrainiumNeuronSentinel(neuron_cores=64, s3_express_latency_ms=1.2).optimize_neuron_pipeline(
        batch_size=256, sequence_length=32768
    )
    ok = (
        res.get("status") == "NEURON_PIPELINE_OPTIMAL"
        and float(res.get("throughput_tokens_per_sec", 0)) > 0
        and float(res.get("tokens_per_core", 0)) > 0
        and isinstance(res.get("fingerprint"), str)
        and len(res.get("fingerprint", "")) == 64
    )
    out = {
        "status": res.get("status"),
        "throughput_tokens_per_sec": res.get("throughput_tokens_per_sec"),
        "tokens_per_core": res.get("tokens_per_core"),
        "fingerprint": res.get("fingerprint"),
        "expected_status": "NEURON_PIPELINE_OPTIMAL",
        "ok": ok,
    }
    print(json.dumps(out, sort_keys=True))
    return 0 if ok else 1
if __name__ == "__main__":
    raise SystemExit(main())
