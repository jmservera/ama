---
title: Issue 144 permit SQL E5 correction plan
description: Plan for the single admitted E5 correction
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e5-correction-1111
---

## Steps

1. Worker lifecycle: record the thread only after `start()` returns; `finish_worker` joins only that thread, collecting join exceptions and a live worker into `errors`. After the ExitStack unwinds on every path: attach any captured worker exception (with formatted traceback) to the primary as a note, or re-raise it when there is no primary; any cleanup error or live worker raises `InvalidWitness` chained from the primary.
2. Isolation: `assert_isolated(environ, cwd)` validates a launcher-written private manifest `ZF_SCRATCH_MANIFEST` (schema `zf-scratch/1`, mode 0600, owned by the uid): exact root (not a general-purpose parent, no symlink, private owned dir, device/inode bound) and exact tmp/home/data/state/cwd paths, each strictly under the root, private and owned, and equal to the resolved actual values.
3. Case 3: read the permitted marker with `service._markers(db, tid)` and assert its stored `issued_at` equals the returned one (label `E1-ISSUED-AT`).
4. Keep seven methods, labels and the N1/N2 matrix.

## Validation

* HARNESS-ONLY synthetic probes (external, duck-typed fakes, no SQL): worker-start failure, primary plus worker error, rollback failure, live worker, isolation misbinding versus genuine scratch. Run against the old aff1 module first to preserve its adverse behaviour, then the new module.
* Focused Ruff, format, strict mypy, 15 SQLite selectors, 7 flag-unset skips, discovery 7.
* Reuse old V only after an origin and byte-identity probe against a new snapshot; otherwise stop for a fresh environment.

## Not done

SQL, container, heavy lock, mutants, publication, full gates.
