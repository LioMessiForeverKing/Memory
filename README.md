Memory Lab
==========

A small playground to explore memory-like algorithms and phenomena: Hopfield networks, Bloom filters, cache replacement (LRU/LFU), and spaced repetition.

Quickstart
----------

1) Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Run the Hopfield demo:

```bash
python scripts/demo_hopfield.py
```

3) Open the notebook playground:

```bash
jupyter notebook notebooks/MemoryPlayground.ipynb
```

Project Structure
-----------------

```
src/
  memory_lab/
    __init__.py
    hopfield.py
scripts/
  demo_hopfield.py
notebooks/
  MemoryPlayground.ipynb
tests/
  test_hopfield.py
```

Goals
-----

- Compare recall accuracy, capacity, and noise tolerance across patterns for Hopfield.
- Explore Bloom filter false positive rates under different parameters.
- Simulate cache hit/miss tradeoffs for LRU/LFU under synthetic traces.
- Prototype a spaced-repetition scheduler (SM-2 baseline) and compare review loads.

Contributing
------------

This is a personal playground. PRs/issues welcome if you spot bugs or have fun ideas.


