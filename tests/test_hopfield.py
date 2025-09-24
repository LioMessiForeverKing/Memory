import numpy as np
from memory_lab import HopfieldNetwork


def test_hopfield_recall_basic():
	net = HopfieldNetwork(num_units=16)
	patterns = np.array([
		[1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1],
		[-1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1],
		[1, 1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1],
	])
	net.train(patterns)

	for p in patterns:
		recalled = net.recall(p, max_steps=20, synchronous=True)
		assert np.array_equal(recalled, p)


def test_hopfield_noise_tolerance():
	rng = np.random.default_rng(0)
	n = 32
	net = HopfieldNetwork(num_units=n)
	patterns = rng.choice([-1, 1], size=(4, n))
	net.train(patterns)
	target = patterns[0]
	noisy = HopfieldNetwork.flip_bits(target, num_flips=4, rng=rng)
	recalled = net.recall(noisy, max_steps=50, synchronous=True)
	# Often recalls exactly; at least should be closer than noisy
	assert (recalled == target).sum() >= (noisy == target).sum()
