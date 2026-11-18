# Issue 223 comparison slice changes (2026-11-14)

* `src/agents/src/zava_forward/agents/review_effectiveness.py`: new `comparison()`; report key `comparison`; CLI prints per-panel detection rate, corrections and effort delta versus workflow-only.
* `src/agents/tests/test_review_effectiveness.py`: new comparison test.
* Validation: ruff check and format clean; 35 tests OK (run with local `PYTHONPATH` because the editable install points at another checkout).
* Not run: full local gate (additive reporting only; focused tier). No hosted CI observed; not pushed.
