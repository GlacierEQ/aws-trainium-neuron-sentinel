from __future__ import annotations

import unittest

from src.workload_passport import (
    PASSPORT_EVIDENCE_STATE,
    ExecutionScope,
    assert_scope,
    build_passport,
    verify_passport,
)


class WorkloadPassportTests(unittest.TestCase):
    def _passport(self) -> dict[str, object]:
        return build_passport(
            ExecutionScope(
                account_alias="research-sandbox",
                region="us-west-2",
                accelerator_family="trainium-modeled",
                workload_id="reasoning-batch-001",
            ),
            {"tokens_total": 4096, "cores": 8},
            {"latency_ms": 1.2, "modeled": True},
            source_sha="a" * 40,
        )

    def test_passport_is_deterministic_scope_bound_and_non_operational(self) -> None:
        first = self._passport()
        second = self._passport()
        self.assertEqual(first, second)
        self.assertTrue(verify_passport(first))
        self.assertEqual(first["evidence_state"], PASSPORT_EVIDENCE_STATE)
        self.assertFalse(first["aws_api_call"])
        self.assertFalse(first["hardware_execution"])
        self.assertFalse(first["operational_authority"])
        assert_scope(first, account_alias="research-sandbox", region="us-west-2")

    def test_tamper_and_cross_scope_replay_fail_closed(self) -> None:
        passport = self._passport()
        passport["source_sha"] = "b" * 40
        self.assertFalse(verify_passport(passport))
        with self.assertRaises(ValueError):
            assert_scope(passport, account_alias="research-sandbox", region="us-west-2")

        clean = self._passport()
        with self.assertRaises(ValueError, msg="cross-account replay must fail"):
            assert_scope(clean, account_alias="production", region="us-west-2")
        with self.assertRaises(ValueError, msg="cross-region replay must fail"):
            assert_scope(clean, account_alias="research-sandbox", region="us-east-1")

    def test_parent_receipt_is_validated(self) -> None:
        scope = ExecutionScope("sandbox", "us-west-2", "trainium-modeled", "child")
        with self.assertRaises(ValueError):
            build_passport(
                scope,
                {},
                {},
                source_sha="a" * 40,
                parent_receipt_sha256="bad",
            )

    def test_empty_scope_fields_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            build_passport(
                ExecutionScope("", "us-west-2", "trainium-modeled", "job"),
                {},
                {},
                source_sha="a" * 40,
            )


if __name__ == "__main__":
    unittest.main()
