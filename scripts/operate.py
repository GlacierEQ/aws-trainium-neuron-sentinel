#!/usr/bin/env python3
"""Cold-start: AWSTrainiumNeuronSentinel — exact mechanism values for fixed inputs."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from aws_trainium_neuron_sentinel import AWSTrainiumNeuronSentinel

# Fixed operate inputs (representative). Expected values from shipped formula:
# tokens_total = batch_size * sequence_length = 256 * 32768 = 8388608
# tokens_per_core = tokens_total / neuron_cores = 8388608 / 64 = 131072.0
# throughput = round((tokens_total / max(s3_express_latency_ms, 0.1)) * 1000.0, 1)
#            = round((8388608 / 1.2) * 1000.0, 1) = 6990506666.7
EXPECTED_TOKENS_PER_CORE = 131072.0
EXPECTED_THROUGHPUT = 6990506666.7
EXPECTED_STATUS = "NEURON_PIPELINE_OPTIMAL"
NEURON_CORES = 64
S3_LAT_MS = 1.2
BATCH = 256
SEQ = 32768

def main() -> int:
    res = AWSTrainiumNeuronSentinel(
        neuron_cores=NEURON_CORES, s3_express_latency_ms=S3_LAT_MS
    ).optimize_neuron_pipeline(batch_size=BATCH, sequence_length=SEQ)
    ok = (
        res.get("status") == EXPECTED_STATUS
        and res.get("tokens_per_core") == EXPECTED_TOKENS_PER_CORE
        and res.get("throughput_tokens_per_sec") == EXPECTED_THROUGHPUT
        and res.get("tokens_total") == BATCH * SEQ
        and res.get("neuron_cores") == NEURON_CORES
        and isinstance(res.get("fingerprint"), str)
        and len(res["fingerprint"]) == 64
    )
    out = {
        "status": res.get("status"),
        "tokens_total": res.get("tokens_total"),
        "tokens_per_core": res.get("tokens_per_core"),
        "throughput_tokens_per_sec": res.get("throughput_tokens_per_sec"),
        "fingerprint": res.get("fingerprint"),
        "expected_tokens_per_core": EXPECTED_TOKENS_PER_CORE,
        "expected_throughput_tokens_per_sec": EXPECTED_THROUGHPUT,
        "expected_status": EXPECTED_STATUS,
        "ok": ok,
    }
    print(json.dumps(out, sort_keys=True))
    return 0 if ok else 1
if __name__ == "__main__":
    raise SystemExit(main())
