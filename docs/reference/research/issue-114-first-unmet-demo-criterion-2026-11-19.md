---
title: Issue 114 first unmet demo criterion
description: Per-criterion proven or unproven record for #114 on the synthetic demo, 2026-11-19
ms.date: 2026-11-19
ms.topic: reference
---

Refs #114. Scope: synthetic desktop demo; owner decisions of 2026-11-18. Base `910adb0a1`. No Azure resource created, no credentials read, no source change.

## Per-criterion result

| Criterion | Ticked | Proven for the demo | Evidence |
| --- | --- | --- | --- |
| Per-year audit and ledger digest verification proven by test before reliance | No | Proven by test on the repository code; unproven on the deployed image | Below |
| Measured load, latency and cost against PRD targets | Yes | Not re-run | [Live load note](./sql-ledger-live-2026-11-18.md) |
| Backup, restore and deletion re-application (DH-005) | Yes | Not re-run | Same note |

## Evidence

* Command, from `src/core`: `PYTHONPATH=src:tests python3 -m unittest test_recovery test_sqlstore test_ledger_digest_blob -q`. Result: 62 tests OK in 30.2 s.
* Covering tests: `test_recovery` (each year alone and with sealed digests, one-year edit, dropped sealed year, malformed digests fail closed, pre-reliance blocks tamper and unsealed years), `test_sqlstore` (multi-year pre-reliance, audit head mismatch, `MssqlStore` inherits the check), `test_ledger_digest_blob` (multi-year blob chain, mutation, truncation, missing anchors).
* No test gap was found, so no code or test was added.

## Not provable on the deployed demo

* The deployed image predates `verify_ledger_before_reliance` on `MssqlStore` ([earlier note](./issue-114-live-reverify-2026-11-18.md)); live data holds one calendar year, so no past year can be sealed.
* Closing that needs an image roll and a `VIEW LEDGER CONTENT` identity: deployment changes outside the owner's 2026-11-18 authorisation.

Tier: FOCUSED (no source change). `rpi-checks.py --all` not run.
