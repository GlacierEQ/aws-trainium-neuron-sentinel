from __future__ import annotations
import unittest
from src.aws_trainium_neuron_sentinel import AWSTrainiumNeuronSentinel

class Adv(unittest.TestCase):
    def test_zero_cores_rejected(self):
        with self.assertRaises(ValueError):
            AWSTrainiumNeuronSentinel(neuron_cores=0)
    def test_pipeline_positive(self):
        res = AWSTrainiumNeuronSentinel(neuron_cores=8, s3_express_latency_ms=1.0).optimize_neuron_pipeline(8, 128)
        self.assertEqual(res["status"], "NEURON_PIPELINE_OPTIMAL")
        self.assertGreater(res["throughput_tokens_per_sec"], 0)
        self.assertEqual(len(res["fingerprint"]), 64)
    def test_fingerprint_stable(self):
        s = AWSTrainiumNeuronSentinel(neuron_cores=4, s3_express_latency_ms=1.0)
        a = s.optimize_neuron_pipeline(4, 16)
        b = s.optimize_neuron_pipeline(4, 16)
        self.assertEqual(a["fingerprint"], b["fingerprint"])

if __name__ == "__main__":
    unittest.main()
