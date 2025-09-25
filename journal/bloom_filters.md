# Bloom Filters: Learning Journal

## Why This
I want to understand how memory can answer "have I seen this before?" using tiny space and accepting some uncertainty.

## What I Built
- BloomFilter with configurable size (m) and hash count (k)
- Helpers to pick optimal m, k for target items (n) and false-positive rate (p)
- Demo that measures empirical false positive rate and compares to theory

## Early Results (placeholders to fill)
- n=1,000, p=0.03 → theory vs empirical close (±0.005)
- n=5,000, p=0.01 → bits per item ~9–10, good match
- n=20,000, p=0.10 → very compact but higher FP, as expected

## Concepts
- False positive (FP): says "present" for an element never inserted
- No false negatives: inserted items always appear present (if implementation correct)
- Space vs accuracy: m (bits) and k (hash count) control FP and memory footprint
- Optimal k ≈ (m/n) ln 2; m ≈ -n ln p / (ln 2)^2

## Questions
- How does the empirical FP rate converge to theory with small n?
- How sensitive is FP to imperfect hash choices?
- What is the best k for practical runtimes vs accuracy?

## Next
- Run the demo across n and p
- Record measured FP into this journal and plot trends
