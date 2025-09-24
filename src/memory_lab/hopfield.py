import numpy as np
from typing import Iterable, Optional


class HopfieldNetwork:
	"""Classic Hopfield network using bipolar {-1, +1} representation.

	- Training via Hebbian learning on provided patterns
	- Synchronous or asynchronous update during recall
	- Supports deterministic updates; tie-break uses sign(0) = +1 by default
	"""

	def __init__(self, num_units: int):
		if num_units <= 0:
			raise ValueError("num_units must be positive")
		self.num_units = num_units
		self.weights = np.zeros((num_units, num_units), dtype=float)

	@staticmethod
	def to_bipolar(pattern: Iterable[int]) -> np.ndarray:
		arr = np.asarray(list(pattern), dtype=int)
		# Map {0,1} -> {-1,+1} if given as binary
		unique_vals = set(arr.tolist())
		if unique_vals.issubset({0, 1}):
			arr = np.where(arr == 0, -1, 1)
		else:
			# Validate already bipolar
			if not unique_vals.issubset({-1, 1}):
				raise ValueError("Patterns must be binary {0,1} or bipolar {-1,1}")
		return arr.astype(int)

	def train(self, patterns: Iterable[Iterable[int]]) -> None:
		"""Hebbian learning: W = sum(p p^T), with zeroed diagonal."""
		W = np.zeros_like(self.weights)
		count = 0
		for p in patterns:
			vec = self.to_bipolar(p).reshape(-1)
			if vec.shape[0] != self.num_units:
				raise ValueError("Pattern length does not match network size")
			W += np.outer(vec, vec)
			count += 1
		if count == 0:
			raise ValueError("No patterns provided")
		# Remove self-connections
		np.fill_diagonal(W, 0.0)
		self.weights = W / count

	def energy(self, state: Iterable[int]) -> float:
		vec = self.to_bipolar(state)
		return -0.5 * float(vec.T @ self.weights @ vec)

	def recall(
		self,
		initial_state: Iterable[int],
		max_steps: int = 50,
		synchronous: bool = True,
		return_trajectory: bool = False,
	) -> np.ndarray | tuple[np.ndarray, list[np.ndarray]]:
		"""Run network dynamics until convergence or max_steps.

		Returns the final state, optionally with the trajectory of states.
		"""
		state = self.to_bipolar(initial_state).copy()
		trajectory: list[np.ndarray] = [state.copy()]

		for _ in range(max_steps):
			prev_state = state.copy()
			if synchronous:
				net = self.weights @ state
				state = np.where(net >= 0, 1, -1)
			else:
				# Asynchronous: update units one by one in fixed order
				for i in range(self.num_units):
					activation = float(self.weights[i, :] @ state)
					state[i] = 1 if activation >= 0 else -1

			trajectory.append(state.copy())
			if np.array_equal(state, prev_state):
				break

		if return_trajectory:
			return state, trajectory
		return state

	@staticmethod
	def flip_bits(pattern: Iterable[int], num_flips: int, rng: Optional[np.random.Generator] = None) -> np.ndarray:
		"""Return a copy with num_flips positions inverted."""
		vec = HopfieldNetwork.to_bipolar(pattern).copy()
		n = vec.shape[0]
		if not 0 <= num_flips <= n:
			raise ValueError("num_flips must be in [0, len(pattern)]")
		rng = rng or np.random.default_rng()
		indices = rng.choice(n, size=num_flips, replace=False)
		vec[indices] *= -1
		return vec
