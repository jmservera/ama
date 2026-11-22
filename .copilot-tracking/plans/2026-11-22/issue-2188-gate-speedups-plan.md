---
title: Plan for issue 2188 shard retry
date: 2026-11-22
---

## Phases

* P1: tools/rpi-checks.py: collision-safe log naming; on a failed test-shard command (exit not 124/127/130, not interrupted) move the failed row to `self.retries`, rerun once; persist `retries` in the receipt.
* P2: `validate_receipt`: validate `retries` (list of dicts, group in executed or inherited groups, log in `files` with matching sha, exit code positive and not 124/127/130; at most one per shard command; passing receipts only keep retries that were followed by passing rows).
* P3: tests in tools/test_rpi_checks.py: retry passes and is recorded; second failure still raises; timeout is not retried; verify rejects a tampered retry log and malformed retries.
* P4: docs in tools README/guide if the gate options are described; changes record with per-criterion table.

See [details](../../details/2026-11-22/issue-2188-gate-speedups-details.md).

## Critique disposition

Executed once: [critique](../../critique/2026-11-22/issue-2188-gate-speedups-critique.md).
