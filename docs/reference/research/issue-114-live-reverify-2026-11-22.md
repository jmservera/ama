---
title: Issue 114 live re-verification (demo), 2026-11-22
description: Re-check of the durable Azure SQL store with ledger audit against merged code and the redeployed demo API, with a per-criterion proven or unproven table
ms.date: 2026-11-22
ms.topic: reference
---

Refs #114. Synthetic desktop demo, resource group `ama`, owner decisions of 2026-11-18. Azure use was read-only; nothing was created. No credentials were read or recorded. Base `6fd6e3f838`. Tier FOCUSED (documentation only).

## Per-criterion result

All three criteria of #114 are already ticked. The table records what this run re-proved.

| Criterion | Proven for the demo | Evidence |
| --- | --- | --- |
| Per-year audit and ledger digest verification proven by test before reliance | Proven by test on the repository code. The deployed image is now very likely to contain it, but this is an inference, not a direct proof | Below |
| Measured load, latency and cost against PRD targets | Not re-run; earlier evidence stands | [Live load note](./sql-ledger-live-2026-11-18.md), [R2 note](./sql-ledger-live-r2-2026-11-18.md) |
| Backup, restore and deletion re-application (DH-005) | Not re-run; earlier evidence stands | Same notes |

## Commands and outputs

* From `src/core`: `PYTHONPATH=src:tests python3 -m unittest test_recovery test_sqlstore test_ledger_digest_blob -q`. Result: 62 tests, OK, 40.0 s. They cover each year alone and with sealed digests, one-year edits, dropped sealed years, malformed or swapped digests, and reliance blocked on tamper or unsealed past years.
* `verify_ledger_before_reliance` lives in `src/core/.../store.py` (line 336, called at line 595) and is inherited by `MssqlStore`; it was added by commit `5cb2c60278` on 2026-11-18.
* Read-only `az containerapp show -g ama -n ca-cutover-test-demo-api`: revision `ca-cutover-test-demo-api--0000053`, Running, image `zava-forward-api@sha256:065628c9...`. This differs from the digest `5368f4e4...` of revision 0000033, which the [2026-11-18 re-verification](./issue-114-live-reverify-2026-11-18.md) found without `verify_ledger_before_reliance`.
* Revision 0000053 was created 2026-11-22T19:38:35Z, four days after the merge, so the image was built after the code landed. `/healthz` returns 200; `/health` and `/version` need sign-in (401).

## Not provable for the demo

* That the deployed image contains the method. The registry `crcutovertestrzsrg` rejects this identity (public access firewall), no build or version value is exposed in the environment, and the authenticated endpoints were not exercised.
* A sealed past year on live data: the live database holds one calendar year, and sealing needs a `VIEW LEDGER CONTENT` identity, a deployment change outside the owner's authorisation.
* Load, latency, cost and DH-005 were not repeated; no drill is authorised.

## Gap assessment

No test or code gap found; no source change made.
