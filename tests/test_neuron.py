"""Test suite for C++ Trainium Neuron executor."""

import unittest


class TrainiumNeuronSim:
    def compute_gflops(self, batch: int, hidden: int) -> float:
        return (2.0 * batch * hidden) / 1e9


class TestTrainiumNeuron(unittest.TestCase):
    def test_gflops_computation(self):
        sim = TrainiumNeuronSim()
        gflops = sim.compute_gflops(32, 4096)
        self.assertGreater(gflops, 0.0)


if __name__ == "__main__":
    unittest.main()
