---
title: Issue 107 release-invariant classifier correction changes
description: Change record for the C2 release-state classifier correction
ms.date: 2026-11-17
---

## Status

Opened before implement-start. No source edit has occurred at this point; entries are appended as work proceeds.

## Planned files

* `src/api/tests/test_old_image_sql_probe.py` (failing-first regressions, fixture precondition)
* `src/api/checks/old_image_sql_probe.py` (judge release invariant)
* `src/api/README.md` (one judging sentence)

## Log

* Tests first (`test_old_image_sql_probe.py`): fixture `after_mutation` mismatch row now active with the MUTATED version (precondition, must stay ACCEPTED); new Judge tests for an active MUTATED row after the mismatch worker, approvals restored only in `after_remaining` or `after_larger`, unproved mismatch completion, lost/malformed/unbound release state, proved violation beside a lost bound row, and unrelated rows unable to establish a trigger. Failing-first log `failing-first-1.log`: exit 1, 11 failures of 20 Judge tests.
* Judge (`old_image_sql_probe.py`): `release_state` and `completed` helpers; release IDs bound from `after_provision`; revocation and mutation read-backs bound to those IDs; `audit` replaces the MUTATED exemption and runs on `after_revoked_restart`, `after_mismatched_restart`, `after_remaining`, `after_larger` (mismatched capability gated on completed supported execute and re-invoke); lost or malformed state is INSUFFICIENT.
* README: one judging paragraph extended.
* No application, store, policy, schema, network, lifecycle, budget, dependency or gate change.

## Validation (own evidence root, retained unique logs)

* Judge tests after change `passing-judge-1.log`: 20 tests OK. Probe module `passing-probe-2/3/4.log`: 40 tests OK, no skips (`passing-probe-1.log` exit 1 was a wrong invocation, missing tests path for the self-test import; retained).
* Related batch: `test_assistant_release` 65 tests OK with 7 skips (MssqlUnleasedRevocation SQL-gated, unchanged), restart non-replenishment 14 OK, RAI restart reconstruction 3 OK, restart audit 1 OK.
* Ruff check clean, Ruff format clean. Strict mypy (`mypy-2.log`): no error in the changed code; two `no-untyped-call` on unchanged `config` import lines (1255, 1417) and unrelated pre-existing import-not-found/other errors elsewhere in this venv.
* Labelled current-source SQLite self-test `selftest-1.log`: ACCEPTED, not old-image evidence.
* Ignored build leftovers from installing the distributions: `src/{core,agents,api}/build/` and `src/*/src/*.egg-info/`; none deleted.
