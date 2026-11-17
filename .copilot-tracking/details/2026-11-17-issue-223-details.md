---
title: Issue 223 phase details
ms.date: 2026-11-17
---

## Phase 1

Panels use the same `Panel` signature. `misses(cls)` returns accept for the proposal whose `defect` equals `cls`, otherwise `competent`. `over_reject` returns `reject` with reason `"[source: <first case label>]"`. Run each through `run_panel` in its own temp dir. A missed class panel must have `gate_passed` False, detected == defects - 1 and the missed row not gate-satisfied. Over-reject must have gate_passed False and `false_rejects` equal to the control count.

## Phase 2

Assert both checks true, per-class sensitivity rows, and a mutation test that patches `gate_satisfied` to always accept and expects the checks to turn false.

## Phase 3

README under the review effectiveness section; log entry in `docs/reference/log.md` only if the README is a knowledge-base file (it is not; skip log). Validation: unittest, mypy src/agents, ruff format check.
