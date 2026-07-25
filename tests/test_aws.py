"""Test suite for AWS Trainium Neuron Sentinel solution."""
import unittest
from aws_trainium_neuron_sentinel import AWSTrainiumNeuronSentinel

class TestAWSTrainiumNeuronSentinel(unittest.TestCase):

    def test_neuron_pipeline(self):
        sentinel = AWSTrainiumNeuronSentinel(neuron_cores=64, s3_express_latency_ms=1.2)
        res = sentinel.optimize_neuron_pipeline(batch_size=256, sequence_length=32768)
        
        self.assertEqual(res["status"], "NEURON_PIPELINE_OPTIMAL")
        self.assertTrue(res["throughput_tokens_per_sec"] > 0)

if __name__ == "__main__":
    unittest.main()
