---
title: Issue 114 live rerun changes
ms.date: 2026-11-18
---

Refs #114. Tier FOCUSED (no `src/` change; no SQL schema, deployment or infrastructure change on the repository side; live work was read-only).

## Changes

* Added docs/reference/research/sql-ledger-live-r2-2026-11-18.md, probe.py and probe-job.log; updated docs/reference/README.md and docs/reference/log.md.
* Azure: created and deleted throwaway job `job-114-r2-probe` (verified absent). One failed execution preserved in the note. No database write, no permission or image change.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Per-year audit and digest verification proven by test before reliance | Partly proven | 62 tests pass; live tamper and per-year checks on live-shaped data; deployed image lacks `verify_ledger_before_reliance`; no multi-year live data; native check denied (`VIEW LEDGER CONTENT`) |
| 2 Measured load, latency, cost vs PRD targets | Proven at demo scale | Prior note: all four p95 limits met, cost below USD 0.15; import preview and bulk edit untested |
| 3 Backup, restore, deletion re-application (DH-005) | Proven at demo scale | Prior note and #145 note; geo-restore and native post-restore ledger check not proven |

## Validation

* `src/core`: `PYTHONPATH=src:tests python3 -m unittest tests.test_recovery tests.test_sqlstore tests.test_ledger_digest_blob`: 62 tests OK.
* mypy, ruff and rpi-checks not run: no source file changed. `rpi-checks.py --all` not run, by instruction.
* Hosted CI for the exact head is not observed (no push).
