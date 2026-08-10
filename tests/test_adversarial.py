from __future__ import annotations

import math
import unittest

from src.aws_trainium_neuron_sentinel import AWSTrainiumNeuronSentinel


class Adv(unittest.TestCase):
    def test_invalid_core_counts_rejected(self) -> None:
        for value in (0, -1, 1.5, True):
            with self.assertRaises((ValueError, TypeError)):
                AWSTrainiumNeuronSentinel(neuron_cores=value)  # type: ignore[arg-type]

    def test_invalid_latency_rejected(self) -> None:
        for value in (0.0, -1.0, math.nan, math.inf, -math.inf):
            with self.assertRaises(ValueError):
                AWSTrainiumNeuronSentinel(s3_express_latency_ms=value)

    def test_invalid_workload_counts_rejected(self) -> None:
        sentinel = AWSTrainiumNeuronSentinel(neuron_cores=8, s3_express_latency_ms=1.0)
        for batch_size, sequence_length in ((0, 1), (1, 0), (1.5, 1), (1, 2.5)):
            with self.assertRaises((ValueError, TypeError)):
                sentinel.model_neuron_pipeline(  # type: ignore[arg-type]
                    batch_size=batch_size, sequence_length=sequence_length
                )

    def test_fingerprint_stable(self) -> None:
        sentinel = AWSTrainiumNeuronSentinel(neuron_cores=4, s3_express_latency_ms=1.0)
        first = sentinel.model_neuron_pipeline(4, 16)
        second = sentinel.model_neuron_pipeline(4, 16)
        self.assertEqual(first, second)
        self.assertEqual(len(first["fingerprint"]), 64)


if __name__ == "__main__":
    unittest.main()
