# Plan: issue #219 authority-holder register (2026-11-01)

Research: [research](../research/2026-11-01-issue-219-rai-release-record-research.md)

## Phases

* [x] Phase 1: add `AUTHORITY_ROLES` and `authority_register()` to `rai_release.py` (pure, no store).
* [x] Phase 2: attach `authority_holders` to the release denial in `assistant_release.denial`.
* [x] Phase 3: tests in `src/core/tests/test_rai_release.py` plus a denial assertion; README note.
* [x] Phase 4: validation (unit tests, ruff check, ruff format --check, mypy for `src/core`).

## Critique (single pass)

Compatible: keep key additive; do not alter `AUTHORITY_GAP` text (existing tests may assert it); holders must stay `None` so no authority is implied. Accepted directly. Verdict: proceed.

## Acceptance mapping

AC5 strengthened (gap itemised per authority). AC1 to AC4 unchanged and already evidenced. AC3 remains constructed-only.

## Correction cycle

Docs/evidence-only fixes for two Copilot review threads; no code change.
