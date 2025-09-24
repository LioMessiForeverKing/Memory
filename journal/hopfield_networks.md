# Hopfield Networks: Learning Journal

## What I Built
A simple Hopfield network implementation that stores patterns as "attractors" in an energy landscape. Give it a noisy pattern, and it iteratively updates until it settles into the closest stored memory.

## Key Discoveries

### 1. Capacity Limits Are Real (Not Bugs)
**Experiment:** Stored 900 patterns in 8000 units, added 800 bits of noise
**Result:** Started with 800 wrong bits, only recovered to 18 wrong bits—not perfect recall
**Why:** Theoretical capacity is ~0.138 × units = ~1104 patterns for random data. I was close to the limit.

**Biology connection:** This mirrors how biological memory works. The hippocampus has finite capacity—store too many similar memories and they interfere. Alzheimer's might be like hitting capacity limits where memories start blending together.

### 2. Graceful Degradation (Not Binary Failure)
**What happened:** Even when recall "failed," it got much closer (800→18 errors). The network didn't just give up—it found a "close enough" solution.

**Biology connection:** Human memory works this way too. We don't remember things perfectly, but we often get "close enough" for practical purposes. This might explain why we can recognize faces even when details are fuzzy.

### 3. Energy Landscapes Create Natural Attractors
**How it works:** Each stored pattern creates a "valley" in an energy landscape. During recall, the network "rolls downhill" until it hits a stable point.

**Biology connection:** This is eerily similar to how neural networks in the brain might work. Memories could be stable states that the brain naturally settles into. Sleep might be like "rolling downhill" to consolidate memories into deeper valleys.

### 4. Pattern Structure Matters Enormously
**Theory:** Random patterns are worst-case for capacity. Orthogonal patterns can store N patterns perfectly. Sparse patterns (few active neurons) store much better.

**Biology connection:** The brain uses "pattern separation" (like in the dentate gyrus) to make memories more orthogonal. This is why similar experiences don't always interfere—the brain actively tries to make them distinct.

### 5. The 8,000 Comma Bug
**What happened:** Typed `num_units = 8,000` instead of `8000`
**Result:** Python created a tuple `(8, 0)` instead of integer `8000`
**Lesson:** Small syntax errors can break everything. Always check your data types!

## Experiments to Try Next

### Capacity Sweep
- Fix units at 1000, vary patterns from 10 to 200
- Plot error rate vs number of stored patterns
- Find the "knee" where recall starts degrading

### Noise Tolerance
- Fix patterns at safe capacity, vary noise from 0% to 50%
- See how much corruption the system can handle
- Compare to human memory robustness

### Pattern Structure Comparison
- Random patterns vs orthogonal patterns vs sparse patterns
- Measure capacity and error rates for each
- Connect to biological pattern separation

### Update Dynamics
- Synchronous (all units update together) vs asynchronous (one at a time)
- Different convergence paths and final states
- More biologically realistic?

## Questions This Raises

1. **Why do biological systems have capacity limits?** Is it a bug or a feature?
2. **How does the brain avoid interference?** Pattern separation, modularity, forgetting?
3. **What's the relationship between energy and consciousness?** Stable states = awareness?
4. **Can we design better artificial memories?** Learning from biological constraints?

## Next Steps
- Implement Bloom filters (probabilistic membership)
- Add cache simulators (LRU/LFU under resource constraints)
- Build spaced repetition scheduler (human learning optimization)

---

*This journal entry captures what I learned from my first Hopfield experiments. Each algorithm reveals different aspects of how memory systems work—and fail.*
