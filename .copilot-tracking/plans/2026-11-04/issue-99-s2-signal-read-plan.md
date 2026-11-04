<!-- markdownlint-disable-file -->

# Plan: issue-99-s2-signal-read

* [x] Phase 1: `load_limits` and `committed_exposure` in exposure_limits.py; `FinanceMixin.exposure_signal` (read-only, finance roles).
* [x] Phase 2: synthetic tests; ruff, mypy, focused unit tests.
* [x] Phase 3: log entry and artifacts.

Details: [phase details](../../details/2026-11-04/issue-99-s2-signal-read-phase-details.md). Tier: focused (no SQL, schema, infrastructure or deployment change). Critique: one pass, no conflicts; limits file is read-only input, absent or malformed gives Held. Later slices: S3 store persistence and API route (SQL tier), S4 UI panel (Fluent 2, WCAG, manual path).
