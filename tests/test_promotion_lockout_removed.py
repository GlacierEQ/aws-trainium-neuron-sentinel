from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_secret_bound_promotion_artifacts_are_retired() -> None:
    retired = (
        ROOT / "src" / "promotion_authority.py",
        ROOT / "machine" / "promotion_authority.json",
        ROOT / "tests" / "test_promotion_authority.py",
        ROOT / "scripts" / "verify_promotion_grant.py",
    )
    assert all(not path.exists() for path in retired)


def test_modeled_accelerator_evidence_remains_keyless() -> None:
    proof = json.loads((ROOT / "machine" / "proof_receipt.json").read_text())
    state = json.loads((ROOT / "machine" / "excellence-state.json").read_text())

    assert proof["repository"] == "GlacierEQ/aws-trainium-neuron-sentinel"
    assert proof["source_sha"]
    assert state["promotion_authority"]["status"] == "RETIRED_KEYLESS"
    assert (
        "no Trainium or Inferentia hardware execution or measurement"
        in state["nonclaims"]
    )
