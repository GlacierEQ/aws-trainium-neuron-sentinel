#!/usr/bin/env python3
"""Fail-closed truth checks for the modeled Trainium/Inferentia study."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"PUBLIC_TRUTH_FAIL: {message}")


def main() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    normalized = readme.replace("**", "").replace("`", "")
    caps = json.loads((ROOT / "machine/capabilities.json").read_text(encoding="utf-8"))
    state = json.loads((ROOT / "machine/excellence-state.json").read_text(encoding="utf-8"))

    require(
        "MODELED_TRAINIUM_SCENARIO_NOT_AWS_HARDWARE_MEASUREMENT" in readme,
        "modeled evidence token missing",
    )
    require(
        "not affiliated with, endorsed by, or operated by Amazon Web Services" in normalized,
        "AWS non-affiliation boundary missing",
    )
    require(
        "not a hardware optimizer" in normalized,
        "hardware-optimizer nonclaim missing",
    )
    require(
        "does not establish access to AWS Neuron hardware" in normalized,
        "AWS hardware-access boundary missing",
    )

    allowed = {
        "deterministic-accelerator-core-token-partitioning-model",
        "modeled-pipeline-bubble-heuristic",
        "explicit-latency-throughput-upper-bound-estimation",
        "stable-sha256-modeled-result-fingerprints",
        "strict-cpp17-reference-surface-compilation",
    }
    require(set(caps.get("capabilities", [])) == allowed, "capability allowlist drift")
    require(caps.get("operational_authority") is False, "operational authority must be false")
    require(caps.get("aws_neuron_hardware_measurement") is False, "hardware measurement claim must be false")
    require(caps.get("neuronx_cc_execution") is False, "neuronx-cc claim must be false")
    require(
        caps.get("trainium_inferentia_model_execution") is False,
        "Trainium/Inferentia execution claim must be false",
    )
    require(caps.get("s3_express_measurement") is False, "S3 Express measurement claim must be false")
    require(caps.get("live_mcp_apex_integration") is False, "live integration claim must be false")

    require(state.get("principal_state") == "FUNCTIONAL_CANDIDATE", "stale promotion restored")
    require(state.get("operational_authority") is False, "machine state grants operational authority")
    proof = state.get("gates", {}).get("DETERMINISTIC_PROOF_GREEN", {})
    require(proof.get("status") == "PENDING_CANONICAL_CI", "fresh exact-head proof gate missing")

    print("PUBLIC_TRUTH_PASS")


if __name__ == "__main__":
    main()
