---
title: Live proof of the digest mismatch alert on the demo (issue 115)
description: Recorded evidence that the ledger digest verifier reports a forced mismatch on a copy and that the Azure Monitor alert fires, on the synthetic demo
ms.date: 2026-11-18
ms.topic: reference
---

Refs #115. Scope is the synthetic demo in resource group `ama`, run on 2026-11-18 under the owner decisions of that date (live Azure authorised, no drills, no production change). The immutable retention lock is deferred to production (#1908) and was not attempted. No secrets, connection strings or sign-in material are recorded below.

## Result

| Criterion | Status | Evidence |
| --- | --- | --- |
| Digests land in an immutable container with a retention lock | Deferred to production (#1908), already ticked by the owner | Not attempted |
| Scheduled verification alerts on mismatch | Proven for verifier, log marker and Azure Monitor alert; delivery to the ops mailbox and the live cron schedule not proven (see limits) | Sections below |

## Method and observations

All times are UTC, 2026-11-18. The storage account `stcutovertestrzsrg` and the log workspace deny public network access, so every data-plane step ran inside the VNet as a Container Apps job and was read through `az containerapp job logs show`.

1. Baseline. The existing job `job-cutover-test-ledger-verify` was started once through the Container Apps start API with a command override that ran the verifier without `--publish` (read-only), keeping the job's own environment. Two earlier attempts failed because the override replaced the environment; they are preserved as `Failed` executions `...-oluza9i` and `...-zugyt7i` (store opened with the default JSON path). The third execution `...-ibj9kvk` succeeded at 08:06:48 and printed `"intact": true`, `"digests": 2`, `"entries": 996`, `"problems": []` and `LEDGER_DIGEST_OK ledger matches the immutable digests`.
2. Forced mismatch on a copy. A throwaway job `job-cutover-test-ledger-verify-9` (name chosen to match the alert query's `startswith "job-cutover-test-ledger-verify"`; the Container Apps 32-character limit rules out a longer suffix) created container `ledger-digests-copy115`, copied the two anchors from `ledger-digests`, and changed the first character of the head hash in `digest-0000000030.json` in the copy only. The original container was never written. The verifier run against the copy at 08:09:35 reported `check: chain`, `digest_count: 30`, `reason: chain differs from the digest`, then `LEDGER_DIGEST_ALERT ledger does not match the immutable digests` and exit 1 (`VERIFY_EXIT 1`).
3. Alert. Azure Monitor (Alerts Management API) shows the alert `Ledger does not match the immutable digests`, rule `alert-cutover-test-ledger-digest-mismatch` (severity 1, scheduled query on `ContainerAppConsoleLogs`, hourly evaluation, one-hour window), condition `Fired`, state `New`, start 08:18:52, target `log-cutover-test`. Latency from the marker to the alert was about nine minutes.
4. Cleanup. The job deleted both copy blobs and the copy container (HTTP 202 each); the throwaway job was then deleted (activity log: `Delete Container Apps Job` Succeeded; list shows no `verify-9`). The storage account has blob soft delete and versioning enabled, so the deleted copy remains recoverable until the soft-delete retention expires; it holds only a tampered duplicate of two synthetic digests. The fired alert record stays in Azure Monitor as the evidence. Temporary files were kept outside the repository.

## Limits and unproven items

* Delivery of the notification: the action group `ag-cutover-test-ops` has one email receiver named `operations`. The mailbox is not accessible to this run, so receipt of the email is not observed. The alert record being `Fired` is the proof of alerting.
* Cron schedule: the deployed job `job-cutover-test-ledger-verify` has trigger type `Manual`; the last cron-named executions are dated 2026-10-20 to 2026-10-26 although `infra/modules/containerapps.bicep` (`ledgerVerify`) defines the cron `0 2 * * *`; the deployed demo differs from that source, cause not investigated. The mismatch was therefore started by hand, not by a schedule. Reinstating a schedule changes deployed infrastructure and was not done.
* The deployed image predates the retention-posture fields in the repository verifier (output lacks them), so the run proves the chain-digest comparison only, not retention-header checks.
* Query access to the Log Analytics workspace is denied from this host by network rules (`NspValidationFailedError`); marker text was read from the job console stream instead. The workspace network setting was not changed.
* Browser proof is not applicable: the alert has no web surface that this run can sign in to, and Azure portal screenshots were not taken.
