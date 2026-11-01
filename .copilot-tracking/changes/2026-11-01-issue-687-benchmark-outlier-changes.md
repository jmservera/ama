# Issue 687 changes (2026-11-01)

* `src/core/tests/test_sqlreads.py`: added `load_sample`, `_burn`, optional contention via `ZF_BENCH_CONTENTION`, per-read load in timing output, and an assertion message listing all timings and load before and after.
* Validation: test_sqlreads passes; ruff check, ruff format --check and mypy pass for src/core. Contention runs recorded in the research artifact.
* No divergences.
* Review thread fix (PR 689): each CPU burner now registers its cleanup immediately after a successful start, so a failed later start cannot leak earlier burners.
