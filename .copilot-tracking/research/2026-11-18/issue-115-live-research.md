---
title: Issue 115 live verification research
date: 2026-11-18
---

# Research: scheduled digest verification alert (issue 115)

Scope: prove the remaining criterion "Scheduled verification alerts on mismatch" on the synthetic demo (resource group ama). Retention lock is deferred to #1908 and is not attempted.

Disposition: executed. Planning readiness: Ready.

## Findings so far

* Verifier: `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` prints `LEDGER_DIGEST_ALERT` on mismatch and `LEDGER_DIGEST_OK` otherwise.
* Container Apps job `job-cutover-test-ledger-verify` (image zava-forward-orchestrator, command `digest_blob --publish`) has trigger type Manual; seven historical Succeeded runs exist (2026-10-20 to 2026-10-26).
* Alert rule `alert-cutover-test-ledger-digest-mismatch` (scheduled query on ContainerAppConsoleLogs, marker LEDGER_DIGEST_ALERT, hourly) exists with action group `ag-cutover-test-ops`.
* Storage account `stcutovertestrzsrg`, container `ledger-digests`.

## Outcome

Live execution done; full evidence and limits in [the research note](../../../docs/reference/research/digest-verification-alert-live-2026-11-18.md). Baseline OK 08:06:48, forced mismatch on a copy 08:09:35, alert fired 08:18:52, cleanup done. Tier: FOCUSED (documentation only, no src change; live Azure per owner decision).
