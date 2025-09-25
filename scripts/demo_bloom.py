#!/usr/bin/env python3
import os
import math
import random
from memory_lab.bloom import BloomFilter, empirical_false_positive_rate


def make_bytes(seed: int, count: int) -> list[bytes]:
	rng = random.Random(seed)
	return [rng.randbytes(16) for _ in range(count)]


def run_suite(n_items: int, target_fp: float, absent_count: int = 10000) -> None:
	m = BloomFilter.optimal_m_bits(n_items, target_fp)
	k = BloomFilter.optimal_k_hashes(m, n_items)
	bf = BloomFilter(m, k)

	present = make_bytes(1, n_items)
	absent = make_bytes(2, absent_count)

	emp = empirical_false_positive_rate(bf, present, absent)
	theory = bf.estimate_fp_rate(n_items)

	bits_per_item = m / n_items
	print(f"n={n_items} target_p={target_fp:.4f} -> m={m} bits, k={k} (~{bits_per_item:.1f} bits/item)")
	print(f"theory_p={theory:.4f} empirical_p={emp:.4f}")


def main() -> None:
	for n in [1_000, 5_000, 20_000]:
		for p in [0.10, 0.03, 0.01]:
			run_suite(n, p)
			print()


if __name__ == "__main__":
	main()
