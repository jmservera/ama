# Issue 1258 API wiring-test lint diagnostic plan (2026-11-09)

Refs #1258. Diagnostic only. Task `1258-ranking-archive-blob-lint-diagnostic`. Research: `.copilot-tracking/research/2026-11-09-ranking-archive-blob-1258-lint-diagnostic-research.md`. Details: `.copilot-tracking/details/2026-11-09-ranking-archive-blob-1258-lint-diagnostic-details.md`. Critique: `.copilot-tracking/plans/2026-11-09-ranking-archive-blob-1258-lint-diagnostic-critique.md`.

## Scope and non-goals

* In scope: one focused read-only Ruff 0.17.1 check and format-check producer over `server.py`, `test_ranking_publication_wiring.py` and `test_case_journey.py` from `src/api` with the maintained `pyproject.toml`; CI applicability; byte-identity to C5; hashed external logs.
* Out of scope: any source edit, `ruff format` write, `--fix`, `--isolated`, rule selection or suppression, unit tests, mypy, global gate, extra cycle, push, PR, board, deployment, fixing the policy-name guard.

## Phases

* [ ] Phase 1: commit this research, plan, details and critique before any producer run (ordering gate).
* [ ] Phase 2 (Implement, validation only): run the producer; capture exit codes and SHA-256 of raw logs outside the repository; prove blob identity to C5 and `9b1e2567`; prove non-tracking tree equivalence of `HEAD` to `9b1e2567` and tested head `59d8ad8a`.
* [ ] Phase 3: write changes, review and state records; commit tracking-only; write the local handoff.

## Decision rules

* Pinned check fails: publication stays blocked; a new explicit finite owner source-correction grant is needed; no child or other issue's budget is used.
* Pinned check passes: explain precisely why the earlier invocation differed, without rewriting its failure.
