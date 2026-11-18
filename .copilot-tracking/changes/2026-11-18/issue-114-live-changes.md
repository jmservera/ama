---
title: Issue 114 live evidence changes
ms.date: 2026-11-18
---

# Changes (Refs #114, tier FOCUSED, no src change)

## Added

* docs/reference/research/sql-ledger-live-2026-11-18.md (research note)
* docs/reference/research/sql-ledger-live-2026-11-18/ (live_load.py, drill.py, result and log files, screenshot)

## Modified

* docs/reference/README.md (index), docs/reference/log.md (entry)

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| C1 Per-year audit and ledger digest verification proven by test | Proven for main (tests); unproven on the deployed demo image | 62 local tests pass; the deployed image has no `verify_ledger_before_reliance` on MssqlStore and live yearly sealing was not run |
| C2 Measured load, latency and cost against PRD targets | Proven for the demo scale (443 synthetic cases, 30 min, five sessions, two writers) | all four p95 within limits, 0 errors in 14,370 samples; cost estimate from public retail prices, not billing |
| C3 Backup, restore and deletion re-application (DH-005) | Proven for same-server PITR to a throwaway database; cross-server throwaway server not possible | restored ledger head equals the pre-erasure head, register in blob survived, reapply redacted the case, resources deleted |

## Validation

* `git diff` and link check of the research note: all relative links resolve.
* `ruff format --isolated --line-length 100` applied to the two evidence scripts (they are not under `src/` or `infra/`; `ruff check` on them reports style findings, not enforced by src-ci for docs).
* `py_compile` of both scripts passed. Core tests: 62 passed (test_recovery, test_sqlstore, test_ledger_digest_blob).
* mypy not applicable (no `src/<project>` change). `rpi-checks.py --all` not run (tier FOCUSED, no src change).
* Deviations: the witness first refused implement-start (state lacked the changes path), then passed with a dirty-source qualification because evidence files predated it. Scripts were reformatted after the live runs; behaviour unchanged.
* Cleanup verified: throwaway databases, jobs and blob container deleted; session cookie file deleted.
