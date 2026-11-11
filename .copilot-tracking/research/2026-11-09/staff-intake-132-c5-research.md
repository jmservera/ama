---
title: Staff intake 132 C5 research
ms.date: 2026-11-09
---

Corrective cycle C5 of five total (final default; C1 to C4 spent, no reset). Parent task `staff-intake-132-c4`. Research disposition: executed. Planning Readiness: Ready.

## Inputs read

* Independent C4 findings, metadata and read ledger (`independent-132-c4-intake-1109/`), head `8aa22878e`, verdict request_changes, 2 High. Previous four findings are recorded as Addressed.
* Handoff `handoff-132-c4-intake-integrity-1109.md`.
* Parent `feat/demo-quality-workflows-89-1109` is now `a8593a7a8670aab27329a81fedee605b4913e7e9` (equal to `origin/main`). Own branch merge-base is `a04668ae9`.

## Parent movement (merge preview)

`git merge-tree --write-tree HEAD a8593a7a` is clean (tree `a83e1d1f2`). The parent delta is 157 files, mostly AI, assistants, sensor and simulation-lane work. Core `quality.py`, `store.py`, `sqlstore.py`, `mssqlstore.py`, `procurement.py`, `job_pack.py`, `projection.py`, `change_provenance.py`, `hazard.py`, `stock.py`, `resident_decisions.py`, `appointments.py`, `identity.py` and `index.html` are unchanged between `a04668ae9` and `a8593a7a`. `server.py` and `app.js` changed in unrelated assistant and simulation code and merge without conflict. Both intents survive an ordinary merge. Contracts relied on by intake (`submit_quality`, `_independent`, `_quality_staff`, procurement validation) are unchanged.

## Finding 1: worker staff code bypass

* `_worker` bars only the keying-in user's name, email and code, and any value containing `@`.
* `submit_quality` stores `submitted_by` as supplied and `_quality_participants` adds `dict(name=supplied)` plus full identities only for staff whose NAME matches. A worker given as `PM-01` (Pam's code) is stored as a name-only participant.
* `_independent` matches participants on the same key only (`name` against `name`, `code` against `code`), so Pam (name `Pam Lead`, code `PM-01`) is not barred, although the intake view says she is.
* `_quality_staff()` is the existing SQL-aware reader (`SELECT body FROM staff` under `dblock`, or `self.staff` for the JSON store). Use it: it reflects the actual registered staff, not a stale in-memory copy.

## Finding 2: procurement snapshot race (confirmed)

* Intake reads the pack digest, ready flag and work-order resident binding from the in-memory procurement document under the process-local `store.lock`.
* `SqlStore.save` runs validators under `BEGIN IMMEDIATE`: `procurement.validate_sql` returns at once when `store.local.procurement_validation` is None. `_proc_write` skips a local document equal to its snapshot BEFORE comparing the database row. Case rows are checked by rowversion only.
* Withdrawal or reissue by another store changes only `meta.procurement` (no case rowversion change). Intake therefore commits a receipt against a pack that no longer exists.
* The existing contract: when `local.procurement_validation` holds `{user, actor, authority, cases, snapshot, authorities, persisted}`, `validate_sql` (called inside the writer transaction) checks the actor is unchanged, the `meta.procurement` row equals `snapshot`, and each listed case rowversion. `appointments.mark_committed` sets `persisted` after COMMIT. `save` clears the token after commit (line 1256) and `_finish` clears it at outermost lock exit.
* Failure path: when the token is set, `save` skips its own `_discard` on `ConflictError`, but quality's `decision_scope` (via `_quality_operation`) already quarantines pending audit and runs `_discard` under `dblock`, so no extra rollback code is needed; this is verified by the red test, not assumed.
* Lifetime and replacement risk: the token is thread-local, set by `_proc_operation` and appointment code. An intake adapter must refuse to run if a token already exists (never replace another operation's token) and restore `None` in `finally`.
* The snapshot is `store._proc_snap.get("procurement")`. It is the value synced at outermost lock entry (`_SyncLock.__enter__` calls `_sync`, which calls `_proc_sync` via the changed-sequence path), so it equals what the pack was derived from. Take it first, before reading the pack.
* JSON store has no `db`, no token and no cross-process validator; behaviour there is unchanged and stated as a limit.

## Decision

Intake-owned adapter to the EXISTING procurement validation contract. No change to `sqlstore.py`, `procurement.py`, `quality.py` or schema is needed, so no shared-hook admission is requested.

## Evidence plan

* Red first on the combined tree: `sam` captures `PM-01` then `pam` runs the real `quality-accept` route with the resident and safety prerequisites satisfied; a two-store interleave where the second store withdraws (and a second case, reissues) between digest validation and save.
* Positive: unrelated QA (`quil`) accepts; ordinary capture still passes.
* SQLite deterministic interleave; the same test on MSSQL under a nonqueued owned lock admission.

## Limits kept

AC5 escalation gap, no named QA, legal, live or assistive-technology acceptance, synthetic approvals are not consent, JSON store has no cross-process guard, `app.js` retry guard does not cover `staff-intake.js`.
