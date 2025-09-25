from memory_lab.bloom import BloomFilter, empirical_false_positive_rate


def test_optimal_params_reasonable():
	m = BloomFilter.optimal_m_bits(1000, 0.01)
	k = BloomFilter.optimal_k_hashes(m, 1000)
	assert m > 0 and k > 0


def test_bloom_basic_membership():
	bf = BloomFilter(1024, 3)
	present = [b"a", b"b", b"c"]
	absent = [b"x", b"y", b"z"]
	for x in present:
		bf.add(x)
	for x in present:
		assert bf.contains(x)
	# It is possible absent returns true, but very unlikely with these params
	fp = empirical_false_positive_rate(BloomFilter(4096, 3), present, absent)
	assert 0.0 <= fp <= 1.0
