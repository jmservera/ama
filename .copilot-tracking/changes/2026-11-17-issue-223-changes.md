---
title: Issue 223 changes
ms.date: 2026-11-17
---

## Changes

* `src/agents/src/zava_forward/agents/review_effectiveness.py`: added `misses_class` and `over_reject` scripted panels, a `sensitivity` report section, checks `each_missed_defect_class_fails_gate` and `over_rejecting_reviewer_cannot_pass`, and CLI lines.
* `src/agents/tests/test_review_effectiveness.py`: two tests (per-class sensitivity and a mutation test forcing the gate to accept, which turns both checks false).
* `src/agents/README.md`: one sentence on the sensitivity section.

## Validation (FOCUSED)

Run from `src/agents` with `PYTHONPATH=src:../core/src:../core/tests:tests` (the installed user-site package otherwise shadows the worktree).

* `python3 -m unittest test_review_effectiveness -q`: 36 tests OK (34 before).
* CLI: all checks PASS, competent gate PASS, each sensitivity panel gate FAIL.
* `mypy`: no issues in 57 source files. `ruff check .` and `ruff format --check .`: clean.
* `ruff format --isolated --line-length 100 --check src tests` flags 6 files; the two edited files are formatted and the other four are untouched pre-existing differences from the project config.
* Not run: full gate, `rpi-checks.py --all`, other suites (no SQL, security, infrastructure or deployment change).

## Divergences

`implement-start` witness was refused once (state `changes` pointer was null); pointer fixed and retried (log seq 4 refused, seq 5 ok).
