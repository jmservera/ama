---
title: Issue 114 live re-verification (demo)
description: Per-criterion re-check of the open acceptance criterion of #114 on the synthetic demo
ms.date: 2026-11-18
ms.topic: reference
---

Refs #114. Scope: synthetic desktop demo, resource group `ama`, owner decisions of 2026-11-18. Read-only Azure use; nothing was created, so nothing needed deleting. No credentials were read or recorded.

## Per-criterion result

| Criterion | Ticked in issue | Status here | Evidence |
| --- | --- | --- | --- |
| Per-year audit and ledger digest verification proven by test before reliance | No | Proven by tests on main; unproven on the deployed image. Stays unticked | Below |
| Measured load, latency and cost against PRD targets | Yes | Not re-run; see [the live load note](./sql-ledger-live-2026-11-18.md) | Prior note |
| Backup, restore and deletion re-application (DH-005) | Yes | Not re-run; see the same note | Prior note |

## Evidence for criterion 1

* Command, from `src/core`: `PYTHONPATH=src:tests python3 -m unittest test_recovery test_sqlstore test_ledger_digest_blob -q`, base `4c45ae3f`. Result: 62 tests OK in 22.6 s.
* Covered: each year verifies alone and with sealed digests; an edit in one year is reported for that year only; a dropped sealed year, corrupt, swapped or root-mismatched digests and unsealed past years block reliance; a tampered chain is not sealed; the SQL store seals past years once and `MssqlStore` inherits `verify_ledger_before_reliance`; blob digests across 2024 to 2026 verify, and truncation or missing anchors are detected.
* Earlier live-shaped evidence: [the second ledger run](./sql-ledger-live-r2-2026-11-18.md) exercised tamper detection and per-year sealing against live-shaped data.

## Why it cannot be proven on the deployed demo

* The deployed API image is `zava-forward-api@sha256:5368f4e4...` (revision `ca-cutover-test-demo-api--0000032`, Running). The earlier note records that its `MssqlStore` has no `verify_ledger_before_reliance`. Registry access is denied from this host, so the build commit was not re-read.
* Live data holds one calendar year, so no past year is sealable; `/api/audit-check` reported `digests_checked` 0 in the epic audit.
* Closing the gap needs an image roll (a deployment change) and a verifying identity with `VIEW LEDGER CONTENT`. Neither is covered by the owner decisions, so neither was done.

## Not run

`rpi-checks.py --all` and any browser proof: no source change and no web surface for this criterion. Tier: FOCUSED.
