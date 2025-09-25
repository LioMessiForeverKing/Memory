from __future__ import annotations
import math
import mmh3
from typing import Iterable


class BloomFilter:
	"""Simple Bloom filter with k hash functions over an m-bit array.

	- Uses murmur3 (mmh3) with different seeds to simulate k hashes
	- Provides helpers to compute optimal m and k for target n, p
	- Supports empirical false positive measurement
	"""

	def __init__(self, m_bits: int, k_hashes: int):
		if m_bits <= 0 or k_hashes <= 0:
			raise ValueError("m_bits and k_hashes must be positive")
		self.m_bits = int(m_bits)
		self.k_hashes = int(k_hashes)
		self._bits = bytearray((m_bits + 7) // 8)
		self._count = 0

	@staticmethod
	def optimal_m_bits(n_items: int, target_fp: float) -> int:
		if n_items <= 0 or not (0 < target_fp < 1):
			raise ValueError("n_items>0 and 0<p<1 required")
		m = - (n_items * math.log(target_fp)) / (math.log(2) ** 2)
		return max(1, int(math.ceil(m)))

	@staticmethod
	def optimal_k_hashes(m_bits: int, n_items: int) -> int:
		if m_bits <= 0 or n_items <= 0:
			raise ValueError("m_bits>0 and n_items>0 required")
		k = (m_bits / n_items) * math.log(2)
		return max(1, int(round(k)))

	def _set_bit(self, idx: int) -> None:
		byte_index = idx // 8
		bit_offset = idx % 8
		self._bits[byte_index] |= (1 << bit_offset)

	def _get_bit(self, idx: int) -> bool:
		byte_index = idx // 8
		bit_offset = idx % 8
		return (self._bits[byte_index] >> bit_offset) & 1 == 1

	def _indexes(self, item: bytes) -> Iterable[int]:
		# Double hashing: h1, h2 then h_i = h1 + i*h2
		h1 = mmh3.hash(item, 0, signed=False)
		h2 = mmh3.hash(item, 1, signed=False)
		for i in range(self.k_hashes):
			yield (h1 + i * h2) % self.m_bits

	def add(self, item: bytes) -> None:
		for idx in self._indexes(item):
			self._set_bit(idx)
		self._count += 1

	def contains(self, item: bytes) -> bool:
		for idx in self._indexes(item):
			if not self._get_bit(idx):
				return False
		return True

	def estimate_fp_rate(self, n_inserted: int | None = None) -> float:
		"""Theoretical FPR: (1 - e^{-k n / m})^k."""
		n = float(n_inserted if n_inserted is not None else self._count)
		m = float(self.m_bits)
		k = float(self.k_hashes)
		return (1.0 - math.exp(-(k * n) / m)) ** k


def empirical_false_positive_rate(bf: BloomFilter, present: list[bytes], absent: list[bytes]) -> float:
	for x in present:
		bf.add(x)
		
	false_pos = 0
	for y in absent:
		if bf.contains(y):
			false_pos += 1
	return false_pos / max(1, len(absent))
