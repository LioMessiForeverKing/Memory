# Hopfield Networks: Learning Journal

## Why I Built This
I wanted a hands-on way to understand memory systems: how recall works from noisy cues, why capacity limits exist, and how interference shows up. A Hopfield network is a minimal model that demonstrates all of this in a concrete, testable way.

---

## Experiment 1: Small, Clean Case (64 units)
- Units (D): 64
- Stored patterns (N): 5 (random, bipolar {-1, +1})
- Noise added: 8 flipped bits (12.5%)

**Observation**
- Hamming(noisy, target) = 8
- Hamming(recalled, target) = 0
- Converged in 2 steps
- Outcome: Perfect recall from a fairly noisy cue.

**Interpretation**
- With a small number of patterns, the network has well-separated “valleys” (attractors). Even a noisy cue sits in the basin of the correct memory and rolls downhill quickly.

---

## Experiment 2: Scale Up (8000 units, near capacity)
- Units (D): 8000
- Stored patterns (N): 900 (random)
- Noise added: 800 flipped bits (10%)

**Observation**
- Hamming(noisy, target) = 800
- Hamming(recalled, target) = 18 (not zero)
- Converged in 6 steps
- Outcome: Improved a lot but not perfect; recall failed by our strict criterion (exact match).

**Interpretation**
- Classic Hopfield capacity for random patterns ≈ 0.138 × D.
  - For D = 8000 → ≈ 1104 patterns at the edge of reliability.
  - N = 900 is close to this limit, so interference is strong.
- The network still denoised from 800 errors down to 18—this is graceful degradation, not a cliff.
- Likely ended in a spurious attractor (a blend state) or the correct basin but not deep enough to reach the exact stored vector.

---

## A Real-World Bug That Taught Me Something
- I accidentally set `num_units = 8,000` (with a comma) which Python read as a tuple `(8, 0)`, breaking the run.
- Lesson: Even tiny syntax issues can completely change meaning; always sanity-check shapes and types.

---

## What These Results Teach About Memory

### 1) Distributed, content-addressable recall
- You don’t need an index—partial/noisy content is enough to retrieve the memory.
- The system finds the nearest attractor by iterative updates.

### 2) Robustness vs interference is a core tradeoff
- Fewer, more distinct patterns → robust recall.
- More patterns (especially random/correlated) → interference and spurious attractors.

### 3) Graceful degradation is a feature
- Failure is often “close-but-not-exact,” which mirrors human memory (approximate, gist-based recall).

### 4) Pattern statistics matter
- Random patterns are worst-case.
- Orthogonal or sparse patterns massively improve effective capacity.

### 5) Biological parallels
- Hippocampal “pattern separation” (e.g., dentate gyrus) reduces overlap among memories.
- Capacity limits are real in brains; interference, confabulations, and blending align with spurious attractors.
- Consolidation (falling to deeper valleys) and rehearsal map onto energy descent dynamics.

---

## How the Model Works (from first principles)

- Representation: Each memory is a length-D vector with bipolar entries {-1, +1}. Binary {0,1} can be mapped via 0→−1, 1→+1.
- Training (Hebbian): For each stored pattern p, add `p p^T` to the weight matrix; zero the diagonal; average across patterns. Intuition: co-active bits strengthen connections.
- Recall (dynamics): Start from the noisy cue and iteratively update state by sign of input:
  - Synchronous: update all bits at once, `state = sign(W @ state)`.
  - Asynchronous: update one bit at a time (more biologically plausible). 
- Energy: `E = -1/2 * state^T W state` monotonically decreases; the system converges to local minima (attractors).

---

## Lessons Learned (so far)
- Exact recall is easy when N ≪ 0.138×D; it gets progressively harder near capacity.
- “Failure” can still be informative—ending within 18 bits of the target shows strong denoising.
- Noise tolerance depends on both N and the structure of stored patterns.
- Update scheme and initialization can change the path and final attractor.
- Sanity-check types and shapes; large-scale runs amplify small mistakes.

---

## Why This Matters (beyond toy models)
- Shows how memory can be keyless and robust to noise.
- Illuminates unavoidable limits in distributed storage systems.
- Connects to human memory phenomena: interference, false recall, category prototypes, and consolidation.
- Inspires engineering tradeoffs: choose sparsity, modularity, or pattern preprocessing when you need higher capacity.

---

## Practical Guidelines: What Actually Works

### Capacity and Noise Tradeoffs (8000 units)
**Theoretical capacity for random patterns:** ~0.138 × 8000 = ~1104 patterns

**Tested combinations that work:**
- **Very safe (low interference):** 400 patterns (~5% of 8000), noise ≤ 20–30% (1,600–2,400 flips)
- **Safe:** 600 patterns (~7.5%), noise ≤ 15–20% (1,200–1,600 flips) ✅ *Tested: 600 patterns, 1200 flips (15% noise) → Perfect recall*
- **Moderate:** 800 patterns (~10%), noise ≤ 10–15% (800–1,200 flips)
- **Near capacity:** 1000–1100 patterns (~12.5–13.8%), noise ≤ 2.5–5% (200–400 flips)

**Rules of thumb:**
- The closer you get to capacity, the smaller the noise you can tolerate
- If you need more noise tolerance at the same pattern count, use structured/orthogonal or sparse patterns (they interfere less)
- Always stay well below 0.138 × units for reliable recall with random patterns

### What This Means
- **600 patterns + 15% noise = perfect recall** (4 steps to converge)
- **900 patterns + 10% noise = partial recall** (18 bits wrong, not perfect)
- The sweet spot is around 5-10% of capacity for robust, noise-tolerant recall

### Complete Failure Case: When Everything Breaks Down
**Experiment:** 500 patterns in 4000 units, 3000 noise flips (75% corruption)
**Result:** 3000 → 3994 wrong bits (99.85% wrong!) - complete failure
**Why it failed:** Hit both capacity limit (90% of theoretical max) AND massive noise overload (75% corruption) simultaneously

**Follow-up:** 390 patterns in 4000 units, 1460 noise flips (36.5% corruption)
**Result:** 1460 → 1605 wrong bits - still failed, but less catastrophically
**Why:** Still near capacity (390/552 = 70%) with high noise - the network converged to a spurious attractor

**Key insight:** Memory systems have **both** capacity limits AND noise tolerance limits. When you hit both at once, the system breaks down completely and produces worse-than-random results.

## Experiments I Want To Run Next
- Capacity sweep: Fix D, vary N; measure exact recall rate and final Hamming distance; identify the "knee."
- Noise sweep: Fix N (well below capacity), vary noise; find the tolerance curve.
- Pattern structure: Compare random vs orthogonal vs sparse; quantify capacity gains.
- Dynamics: Compare synchronous vs asynchronous updates; measure steps to converge and error.
- Modularity: Split patterns across multiple smaller Hopfield nets; test interference reduction.

---

## Minimal Glossary
- Attractor: A stable state where updates stop changing the pattern.
- Basin of attraction: Set of starting states that converge to the same attractor.
- Spurious attractor: A stable state that is not one of the stored patterns (often a blend).
- Hamming distance: Number of positions where two patterns differ.

---

## One-Line Summary
From 64 units/5 patterns with perfect recall to 8000 units/900 patterns with near-capacity interference, I saw how associative memory excels at denoising yet hits principled limits—just like biological memory systems.
