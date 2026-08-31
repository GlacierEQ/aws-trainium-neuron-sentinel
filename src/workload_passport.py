"""Hash-bound workload scope passports for modeled accelerator scenarios.

A passport binds a local modeled workload to an explicit account alias, region,
accelerator family, source identity, assumptions, and optional predecessor.
It performs no AWS API call and grants no cloud authority.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass

PASSPORT_SCHEMA = "glaciereq.aws-modeled-workload-passport.v1"
PASSPORT_EVIDENCE_STATE = "LOCAL_SCOPE_PASSPORT_NOT_AWS_ACCOUNT_OR_HARDWARE_AUTHORITY"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SOURCE_RE = re.compile(r"^[0-9a-f]{40,64}$")


@dataclass(frozen=True, slots=True)
class ExecutionScope:
    account_alias: str
    region: str
    accelerator_family: str
    workload_id: str

    def to_dict(self) -> dict[str, str]:
        values = {
            "account_alias": self.account_alias,
            "region": self.region,
            "accelerator_family": self.accelerator_family,
            "workload_id": self.workload_id,
        }
        for name, value in values.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text")
        return {name: value.strip() for name, value in values.items()}


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=str
    ).encode("utf-8")


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def build_passport(
    scope: ExecutionScope,
    scenario: Mapping[str, object],
    assumptions: Mapping[str, object],
    *,
    source_sha: str,
    parent_receipt_sha256: str | None = None,
) -> dict[str, object]:
    """Bind a modeled workload to exact scope and provenance."""

    if not _SOURCE_RE.fullmatch(source_sha):
        raise ValueError(
            "source_sha must be a lowercase hexadecimal 40-64 character digest"
        )
    if parent_receipt_sha256 is not None and not _SHA256_RE.fullmatch(
        parent_receipt_sha256
    ):
        raise ValueError("parent_receipt_sha256 must be a lowercase SHA-256 digest")
    if not isinstance(scenario, Mapping) or not isinstance(assumptions, Mapping):
        raise ValueError("scenario and assumptions must be mappings")

    body: dict[str, object] = {
        "schema": PASSPORT_SCHEMA,
        "scope": scope.to_dict(),
        "source_sha": source_sha,
        "scenario_sha256": _digest(dict(scenario)),
        "assumptions_sha256": _digest(dict(assumptions)),
        "parent_receipt_sha256": parent_receipt_sha256,
        "evidence_state": PASSPORT_EVIDENCE_STATE,
        "operational_authority": False,
        "aws_api_call": False,
        "hardware_execution": False,
    }
    body["receipt_sha256"] = _digest(body)
    return body


def verify_passport(passport: Mapping[str, object]) -> bool:
    """Verify the receipt digest over the stored passport body."""

    observed = passport.get("receipt_sha256")
    if not isinstance(observed, str) or not _SHA256_RE.fullmatch(observed):
        return False
    body = {key: value for key, value in passport.items() if key != "receipt_sha256"}
    return _digest(body) == observed


def assert_scope(
    passport: Mapping[str, object],
    *,
    account_alias: str,
    region: str,
) -> None:
    """Fail closed when a passport is replayed into a different declared scope."""

    if not verify_passport(passport):
        raise ValueError("passport integrity verification failed")
    scope = passport.get("scope")
    if not isinstance(scope, Mapping):
        raise ValueError("passport scope is missing")
    if scope.get("account_alias") != account_alias or scope.get("region") != region:
        raise ValueError("passport scope mismatch")
