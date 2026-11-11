---
title: Issue 1360 served-transfer outcome diagnostic research (read-only, no repair grant)
ms.date: 2026-11-10
task_id: 1360-outcome-diagnostic-1110
---

## Disposition and scope

Research executed 2026-11-10 (UTC), after launch (witness seq 1) and research-open (witness seq 2, accepted, no qualifications). The research file was first persisted as a short stub before research-open and completed here in place. Planning Readiness: Ready.

Scope: a read-only product diagnostic of the generic `OSError`/`ValueError` branch of the importer `transfer` command (issue 1360, a static follow-up of the independent parent 73 review). No product, test, configuration or documentation implementation is authorised. Issue number 1360 does not reset the spent 135 C5 allowance (zero left) and creates no repair grant. Status of the claim at this point: STATIC ONLY, not reproduced. It may be called reproduced only after an actual durable counterexample is observed.

## Identities

| Item | Value |
| --- | --- |
| Worktree | `/home/azureuser/source/ama-demo-wt/issue-1360-outcome-diagnostic-1110` |
| Branch | `test/demo-transfer-outcome-diagnostic-1360-1110` |
| Pinned main (HEAD at start) | `fe59ef56a0084dd975fd7e5c342670bb8f788fb0`, worktree clean |
| Own external env | `/tmp/zf-1360-1110/venv` (Python 3.12.3), editable installs of `src/core` and `src/importer` |
| Module origins asserted | `zava_forward.core` and `zava_forward.importer` resolve under the worktree `src/*/src` (checked before any run) |

## Static findings (read from source at the pinned head)

* `__main__.py` `_transfer` (lines 123-164): opens the served store via `open_store`, then calls `transfer(ledger, target)`. Exception arms, in order: `ConflictError` (rolled back, "nothing was recorded"), `CommittedReloadError` ("may be recorded"), `PartiallyRecordedError`, generic `(OSError, ValueError)` ("the served store refused it (...). Nothing was recorded."), database driver errors ("not known whether"). All exit 2 through `_stopped`.
* `exceptions.py` `transfer` only calls `target.record_import_refusals`; it has no knowledge of commit state. The ledger is read only.
* `import_refusals.py` `record_import_refusals` validates, merges by `file:<hash>` ref, then calls `_persist_import_refusals`. `ValueError` raised here (normalisation, `MAX_REFUSALS`) precedes any write.
* `sqlstore.py` `save` (about lines 1130-1270): `BEGIN IMMEDIATE`, validation, row and recommendation writes, `_proc_write` (writes the `import_exceptions` document under an optimistic compare against `_proc_snap`, `ConflictError` otherwise), `_append_audit`, `UPDATE meta seq`, then `COMMIT`. After the commit the in-memory snapshots are updated. Then `cur == self._seq` takes the cheap path (`_seq = new`, no refresh). Only when `cur != self._seq` (another writer bumped `meta seq` since this store last synced) is `_sync()` called, and only `RuntimeError` is translated to `CommittedReloadError`. An `OSError` or `ValueError` from that post-commit `_sync` is not translated.
* `_persist_import_refusals` (about lines 1270-1287): re-raises `CommittedReloadError`; for any other `BaseException` it calls `_discard(pending_before)` (restores snapshots, `_seq = -1`, reloads) and re-raises the original error. In-memory recovery is not evidence of durable rollback.
* `_sync` begins with `_db_seq()` reads and then reloads changed rows. A wrapper on `_sync` that checks its caller is `save` and independently confirms the commit is the narrowest post-commit hook.
* An audit-only commit (`_audit_immediate`) does not bump `meta seq`. A seq-changing independent writer must therefore be a full `save` or a seed merge, not an audit-only call.
* A second writer that records the same `import_exceptions` document makes the first writer's `_proc_write` raise `ConflictError` (pre-commit rollback). That is the existing real-competing-writer test and a different branch from the one under test.

## Existing tests (adjacent fixtures)

`src/importer/tests/test_import_exceptions.py` `TransferFailureTests` (lines 560-637) uses a real SQLite served store, the real CLI via `runpy`, a real competing writer (conflict rollback), and mocks `SqlStore.record_import_refusals` for committed-reload, partial, driver and generic `ValueError` cases. The generic `ValueError` assertion ("Nothing was recorded") rests on a mock at `record_import_refusals`, before any commit. No existing test reaches the post-commit `_sync` generic-error path.

Baseline: `python -m unittest tests.test_import_exceptions` from `src/importer` in the own env, 40 tests, OK (log `/tmp/zf-1360-1110/logs/baseline-import-exceptions.log`).

## Open hypothesis and pre-registered prediction

Hypothesis H1 (unreproduced): with a real `SqlStore.save`, a non-conflicting independent writer commit that changes `meta seq` before the transfer's save, and an `OSError` (and, if cheap, `ValueError`) injected only at the post-commit `_sync`, the transfer CLI exits 2 with "Nothing was recorded", while an independent reopen shows the refusal document and the `recorded_import_refusals` audit entry retained, and a repeat transfer reports `added=0 already_present=1` with no second audit entry.

Disconfirming outcomes to preserve: the injection is never reached; the save raises `ConflictError` first; the committed state is not durable; or the CLI prints a conservative message.

## Unknowns

* Whether any real writer produces a non-conflicting seq change in that window. The injection simulates the I/O failure, not its natural cause, so a reproduction would show the message contract defect, not a naturally observed production `OSError`.
* The finite history of the 135 and 132 allowances is UNKNOWN beyond the owner statement that C5 is spent with zero left.
