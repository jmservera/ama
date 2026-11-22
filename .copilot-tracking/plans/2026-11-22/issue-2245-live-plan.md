# Plan: issue 2245 thread creation 500

Tier: focused (test only, no src change; classification basis: no source, workflow, dependency or Azure change).

* [ ] Phase 1: add `test_thread_creation_takes_the_write_lock_at_most_twice` to `src/core/tests/test_chatthreads.py` (SQL store class); run `test_chatthreads`.
* [ ] Phase 2: write the dated note `docs/reference/research/issue-2245-thread500-2026-11-22.md` with the per-criterion table, index in `docs/reference/README.md` and a log entry.
* [ ] Phase 3: review once, commit locally with `Refs #2245`.
