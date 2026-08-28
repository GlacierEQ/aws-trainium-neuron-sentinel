"""Deterministic accelerator scenario arithmetic inspired by public Trainium concepts.

This module does not execute AWS Neuron, access Trainium/Inferentia hardware,
compile a model with neuronx-cc, query S3 Express, or measure production
throughput. It models token partitioning, a simple pipeline-bubble heuristic,
and a latency-only throughput upper bound from explicit assumptions.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict

EVIDENCE_STATE = "MODELED_TRAINIUM_SCENARIO_NOT_AWS_HARDWARE_MEASUREMENT"


def _digest(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _positive_int(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _positive_finite(name: str, value: float) -> float:
    numeric = float(value)
    if not math.isfinite(numeric) or numeric <= 0:
        raise ValueError(f"{name} must be finite and > 0")
    return numeric


class AWSTrainiumNeuronSentinel:
    """Model accelerator partitioning from explicit local assumptions."""

    def __init__(
        self, neuron_cores: int = 64, s3_express_latency_ms: float = 1.2
    ) -> None:
        self.neuron_cores = _positive_int("neuron_cores", neuron_cores)
        self.s3_express_latency_ms = _positive_finite(
            "s3_express_latency_ms", s3_express_latency_ms
        )

    def model_neuron_pipeline(
        self, batch_size: int = 256, sequence_length: int = 32768
    ) -> Dict[str, Any]:
        """Return deterministic scenario values; no AWS runtime is contacted."""

        batch_size = _positive_int("batch_size", batch_size)
        sequence_length = _positive_int("sequence_length", sequence_length)
        tokens_total = batch_size * sequence_length
        tokens_per_core = tokens_total / self.neuron_cores
        modeled_pipeline_bubble_pct = max(0.8, 12.5 / math.sqrt(self.neuron_cores))
        latency_only_upper_bound_tps = tokens_total / (
            self.s3_express_latency_ms / 1000.0
        )

        body = {
            "neuron_cores_assumption": self.neuron_cores,
            "tokens_total": tokens_total,
            "tokens_per_core": round(tokens_per_core, 6),
            "modeled_pipeline_bubble_percent": round(modeled_pipeline_bubble_pct, 2),
            "latency_only_upper_bound_tokens_per_sec": round(
                latency_only_upper_bound_tps, 1
            ),
            "latency_assumption_ms": self.s3_express_latency_ms,
            "evidence_state": EVIDENCE_STATE,
        }
        body["fingerprint"] = _digest(body)
        return body

    def optimize_neuron_pipeline(
        self, batch_size: int = 256, sequence_length: int = 32768
    ) -> Dict[str, Any]:
        """Compatibility alias for the historical public API."""

        return self.model_neuron_pipeline(
            batch_size=batch_size, sequence_length=sequence_length
        )
