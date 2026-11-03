<!-- markdownlint-disable-file -->
# Plan: gate benchmark for #470 (2026-11-02)

* [ ] 1. Rebase on origin/main; commit research, plan, state (clean HEAD for the gate).
* [ ] 2. Hold the heavy lock, record load and specs, run `--all --jobs 1` then `--all --jobs 2` serially into new external dirs.
* [ ] 3. Extract per-group and total wall time from the receipts; verify both receipts.
* [ ] 4. Add a concise results table with caveats to the "Local RPI gate" section of `src/README.md`.
* [ ] 5. Review, commit, push `ci/gate-benchmark-470`, open PR with `Refs #470` and the numbers.

Critique: not executed as a separate artifact; self-check only (documentation-only change, focused tier plus human review).
