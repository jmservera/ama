# Plan: issue 470 faster local gate (2026-11-01)

Research: [research](../research/2026-11-01-issue-470-faster-local-gate-research.md)

Critique: executed once. Verdict: proceed. Advice to add a benchmark harness rejected as scope creep against the owner's "keep scope tight, no heavy gate" direction.

## Phases

* [x] Phase 1: re-verify the existing gate behaviour with the focused tier (`tools/test_rpi_checks.py` selection, scope and resume tests, ruff, ruff format check, mypy on `tools`).
* [x] Phase 2: record RPI evidence (research, plan, changes, review).
* [x] Phase 3: commit, push, open the PR with `Refs #470` naming unmet criterion 4.

## Out of scope

Full serial and parallel benchmark runs; any change to `tools/rpi-checks.py`.
