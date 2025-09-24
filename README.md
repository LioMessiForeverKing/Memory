Memory Lab
==========

A learning journal for exploring memory phenomena through algorithms. Each experiment teaches something about how memory systems work—and fail.

Current Focus: Hopfield Networks
-------------------------------

**What I'm discovering:**
- Capacity limits aren't bugs—they're fundamental tradeoffs between storage, robustness, and interference
- Random patterns are worst-case; orthogonal/sparse patterns store much better
- Graceful degradation: even "failed" recalls often get much closer to the target
- Energy landscapes create natural attractors—memories as stable valleys

**Key experiments to try:**
- Capacity sweep: How many patterns before recall breaks?
- Noise tolerance: How much corruption can the system handle?
- Pattern structure: Random vs orthogonal vs sparse—which stores better?
- Update dynamics: Sync vs async—different convergence paths?

**Current status:** Basic Hopfield implementation working. Next: Bloom filters, then cache simulators.

**Learning Journal:** [Hopfield Networks](journal/hopfield_networks.md) - Detailed notes on experiments, failures, and biology connections

Project Structure
-----------------

```
src/memory_lab/          # Core algorithms
scripts/                 # Quick experiments  
notebooks/               # Interactive playground
tests/                   # Sanity checks
```

Philosophy
----------

This isn't about building production systems—it's about understanding memory through code. Each algorithm reveals different aspects: associative recall (Hopfield), probabilistic membership (Bloom), resource constraints (caches), learning schedules (spaced repetition).

The goal is to build intuition about how memory works by breaking it.


