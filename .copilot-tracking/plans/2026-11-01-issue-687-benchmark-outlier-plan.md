# Issue 687 plan (2026-11-01)

* [x] Add load sample (load average, CPU count) and a per-read timing summary to the benchmark assertion message and timing lines.
* [x] Add opt-in `ZF_BENCH_CONTENTION=N` CPU burner processes to repeat the benchmark under defined contention.
* [x] Keep the 1,500 ms threshold unchanged; no query or index change.
* [x] Validate: `python3 -m unittest test_sqlreads` in src/core/tests, ruff check, ruff format --check, mypy.
* Critique (single pass): scope is tight; no production code changes; compatible. Verdict: proceed.
