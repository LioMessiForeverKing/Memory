#!/usr/bin/env python3
import numpy as np
from memory_lab import HopfieldNetwork


def make_random_patterns(num_patterns: int, num_units: int, rng: np.random.Generator) -> np.ndarray:
	# Create random bipolar patterns {-1, +1}
	return (rng.random((num_patterns, num_units)) < 0.5).astype(int) * 2 - 1


def hamming_distance(a: np.ndarray, b: np.ndarray) -> int:
	return int(np.sum(a != b))


def main() -> None:
	rng = np.random.default_rng(42)
	num_units = 8000
	num_patterns = 900
	noise_flips = 800

	patterns = make_random_patterns(num_patterns, num_units, rng)
	net = HopfieldNetwork(num_units)
	net.train(patterns)

	idx = 0
	target = patterns[idx]
	noisy = HopfieldNetwork.flip_bits(target, noise_flips, rng)
	recalled, traj = net.recall(noisy, max_steps=50, synchronous=True, return_trajectory=True)

	print(f"Stored patterns: {num_patterns}, units: {num_units}")
	print(f"Noise flips: {noise_flips}")
	print(f"Hamming(noisy, target) = {hamming_distance(noisy, target)}")
	print(f"Hamming(recalled, target) = {hamming_distance(recalled, target)}")
	print(f"Converged in {len(traj)-1} steps")

	# Simple success criterion
	success = hamming_distance(recalled, target) == 0
	print("Recall success:" , success)


if __name__ == "__main__":
	main()
