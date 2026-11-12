---
title: Issue 144 permit SQL E5 correction changes
description: Changes and observed outcomes of the one admitted E5 correction
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e5-correction-1111
---

## Changed

* `src/api/tests/test_permit_sql.py` only (sha256 `2f45a6905337328793b5937c3079e407735cd54484b51b3949d6c7b8520de017`; aff1 version `a5fdab0b...0c`).
  * Worker lifecycle: thread recorded only after a successful `start()`; join errors collected; worker exception attached to the primary or re-raised; cleanup errors or a live worker raise `InvalidWitness` chained from the primary.
  * Isolation: `assert_isolated(environ, cwd)` validates a private launcher manifest (`ZF_SCRATCH_MANIFEST`, `zf-scratch/1`) with exact root, device/inode identity and exact tmp/home/data/state/cwd paths.
  * Case 3 also asserts the durable permitted marker `issued_at` equals the returned value (`Assistants._markers`).
  * Seven methods and labels unchanged.

## Observed (external `144-permit-sql-e5-correction-1111/logs`)

| Check | Exit | Result |
| --- | --- | --- |
| 01 HARNESS-ONLY probe on aff1 module | 0 | Reproduced both findings: start failure became "cannot join thread before it is started"; worker error missing on body failure; `TMPDIR=/tmp` accepted |
| 02 probe on new module before format | 0 | 16 of 16 |
| 04/05 ruff check and format on first E5 edit | 1,1 | One E501 and a format diff; preserved |
| 06 format apply (module only), 07/08 ruff, 09 strict mypy | 0 | Pass, no issues in 2 files |
| 10 probe on final bytes | 0 | 16 of 16 |
| 11 15 SQLite selectors | 0 | Ran 15 OK |
| 12 flag-unset module | 0 | Ran 7 OK (skipped=7), exact reason |
| 13 discovery | 0 | 7 |

Origins (log 03): all module files come from the new snapshot; the editable finders of the reused old V only add old-snapshot paths (identical bytes, verified 699 files) to namespace `__path__`.

## Limits

Probes are HARNESS-ONLY fakes, not SQL or application proof. No SQL, container, lock or mutant run.
