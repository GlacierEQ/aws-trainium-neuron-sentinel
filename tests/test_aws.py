"""Regression tests for the bounded Trainium scenario model."""

from __future__ import annotations

import unittest

from src.aws_trainium_neuron_sentinel import AWSTrainiumNeuronSentinel


class TestAWSTrainiumNeuronSentinel(unittest.TestCase):
    def test_neuron_pipeline_scenario(self) -> None:
        sentinel = AWSTrainiumNeuronSentinel(neuron_cores=64, s3_express_latency_ms=1.2)
        result = sentinel.model_neuron_pipeline(batch_size=256, sequence_length=32768)

        self.assertEqual(
            result["evidence_state"],
            "MODELED_TRAINIUM_SCENARIO_NOT_AWS_HARDWARE_MEASUREMENT",
        )
        self.assertEqual(result["tokens_total"], 256 * 32768)
        self.assertEqual(result["tokens_per_core"], (256 * 32768) / 64)
        self.assertGreater(result["latency_only_upper_bound_tokens_per_sec"], 0)
        self.assertNotIn("status", result)
        self.assertNotIn("throughput_tokens_per_sec", result)
        self.assertEqual(len(result["fingerprint"]), 64)

    def test_historical_api_is_bounded_alias(self) -> None:
        sentinel = AWSTrainiumNeuronSentinel(neuron_cores=8, s3_express_latency_ms=1.0)
        self.assertEqual(
            sentinel.optimize_neuron_pipeline(batch_size=8, sequence_length=128),
            sentinel.model_neuron_pipeline(batch_size=8, sequence_length=128),
        )


if __name__ == "__main__":
    unittest.main()
