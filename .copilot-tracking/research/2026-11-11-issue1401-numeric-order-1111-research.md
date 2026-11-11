---
title: Issue 1401 numeric concern order cycle 1 research
ms.date: 2026-11-11
task_id: 1401-numeric-order-1111
---

## Scope and boundary

Cycle 1 of an owner-authorized maximum of three scoped cycles (owner, 2026-11-11) on existing issue #1401, separate budget 1 of 3 on launch; inherited #133/#89 history is not reset and this is not whole #133/#89 acceptance. Branch `fix/aftercare-numeric-order-1401-1111`, base and head `e691255ff7aae111ef32d585900cf82c3789a78c`, target `main`. PR #1400 merge `64c3f9191a2ffa97ef2dc07245422333ad4d6585` verified as an ancestor (`git merge-base --is-ancestor`, exit 0). Research disposition: executed. No push, PR, issue tick or board write. Issue #1402 (blank/whitespace corruption repair) is a separate queued branch and is not implemented here.

## Evidence consumed

* Issue #1401 body read as data (state OPEN): Medium inherited D5 finding; smallest correction is to restore concerns in validated numeric identifier order independent of JSON insertion order, preserving uniqueness and gap checks; acceptance needs a regression, scoped fix, read/write/restart/replay across supported adapters and an independent exact-head review. The original adverse finding stays open and is not waived.
* `src/core/src/zava_forward/core/aftercare_intake.py`: `_txn` serializes with `json.dumps(doc, sort_keys=True)`; `_validate` and `_register` call `AftercareRegister.from_state(doc["register"])`.
* `src/core/src/zava_forward/core/aftercare_store.py`: `_canon` also uses `sort_keys=True` for `read`, so both layers text-sort recursive keys.
* `src/core/src/zava_forward/core/aftercare.py`: `from_state` enumerated `reg.concerns.items()` in JSON order and required `cid == f"AC-{n:03d}"`; `raise_concern` assigns `len(concerns)+1`.

## Diagnosis

Text sort places `AC-1000` before `AC-101` (and `AC-1000` before `AC-999`), so a register with 1000 or more concerns, as written by the product itself, fails the positional check on the next read and the service raises `StateInvalid` (mapped to a 503/manual route). Up to 999 padded identifiers text order equals numeric order, which hid the defect. Disabling key sorting would alter the canonical text used for snapshot comparison in the adapter's failure classification, so it is rejected; the validation must not be relaxed.

## Observed original failure (unmodified code)

A real run on the unmodified source through the JSON `Store` and `DocumentStateStore` recorded 1001 concerns via `record_concern`; the 1001st call raised `StateInvalid` ("The saved aftercare record is not valid ...") after 105 s (script `/tmp/repro1401.py`, raw output in the handoff).

## Design

In `from_state`, order the stored concerns by the numeric part of canonical `AC-nnn` identifiers (a non-matching key maps to -1), then keep the existing positional check `cid == AC-{n:03d}` over that order. Gaps, non-canonical keys (`AC-0501`, `AC-X`), id/key mismatch and every other record check still raise `ValueError`. No change to intake or adapter serialization, so no schema or format change.

## Adapter and validation prerequisites

* JSON `Store` and `SqlStore` (SQLite) run by default in `tests/test_aftercare_store.py`; the owned SQL Server variant needs `ZF_RESIDENT_MSSQL=1` and `tests/sqlguard.py` admission (label `zf.task`, loopback publish, manifest). Cached `mcr.microsoft.com/mssql/server:2022-latest` is present, `mssql-python` 1.15.0 imports, `/tmp/ama-rpi-heavy.lock` was free under non-queued `flock -n`.
* No cloud, model, deployment, spend or private dataset is used. PYTHONPATH points at this worktree's `src/*` because the installed editable packages resolve to a different checkout.

## Planning Readiness

Ready.
