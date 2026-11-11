---
title: Issue 144 permit SQL E4 plan P2 phase details
description: Gates, command deltas, failure classes and pause conditions for the P2 plan correction
ms.date: 2026-11-11
task_id: issue-144-permit-sql-e4-plan-p2-1111
---

## Phase gates

* Phase A (done): Research and plan correction, artifacts only, no execution.
* G1: same independent reviewer `9e2e122a-295f-46f8-af5a-9e28472a4d06` clears the actual P2 delta. Blocking findings must be resolved first.
* G2: Root explicitly admits implementation, the conditional pip steps and the current nonqueued heavy-resource, container and SQL run. Not given here.
* Phase B (future, same E4): create `src/api/tests/test_permit_sql.py`, author external scripts, run X0 to X10, write dated changes and review records, commit. Phase C: authored review; independent exact-head assessment is Root's.

## Prospective command deltas versus P1 (X numbering unchanged)

* X1: unchanged; the failing probe now also records `import setuptools` absence (`python -c "import setuptools"`, expected exit 1) before any install; the result is preserved.
* X2a: `pip download` pinned `setuptools==80.9.0 wheel==0.45.1 ruff==0.17.1 mypy==2.4.0` into `X/wheelhouse-tools`; runtime download unchanged; wheel hashes in `receipts/wheel-sha256.txt`.
* X2b: offline install of the build backend into V, M1 and M2 (`--no-index --find-links X/wheelhouse-tools`), then the hashed runtime requirements offline.
* X2c: every editable is `pip install --no-build-isolation --no-index --find-links X/wheelhouse-tools --no-deps -e <dir>`; artifacts only under `snap/` and `mut/`.
* X3: unchanged commands; the new module builds its fixture composite with `type()` and has no skipped-import subclass statement.
* X4: unchanged (15 fully qualified ids, Ran 15, OK, zero skips).
* X5: unchanged (Ran 7, skipped=7, discovery count 7).
* X8/X9: the test bodies use the ExitStack cleanup structure, case 6 flow and case 5 collection-count assertion of the plan; origin evidence from both the probe and the test process; per-file snapshot hash listing compared before and after.
* X10: unchanged.

## Failure classification (unchanged and restated)

Source defect only for a fixed-source assertion failure with every setup witness valid (stop on existing #144, no fix, no new issue). Invalid setup: R1 assertion, scratch identity, SPID or `@@TRANCOUNT` change, DMV or headroom miss, `WORKER-STILL-LIVE`, `CLEANUP-ERRORS`, container or resource error. Expected mutant failure: exactly the frozen matrix with labelled `AssertionError`. Anything else on a mutant is INCONCLUSIVE and blocks success. Environment failure (missing or sdist-only wheel, docker, timeout) is blocked or unobserved, never a relaxed pin.

## Pause and resume

Paused after this correction. Resume only on Root's explicit G1 and G2 admission. No canonical phase-witness chain was requested for this launch and none was created or backfilled; this is recorded, not regraded.
