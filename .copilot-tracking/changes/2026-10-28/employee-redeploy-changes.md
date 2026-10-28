---
title: Employee redeploy execution evidence
description: Read-only preservation and blocked one-redeploy attempt
ms.date: 2026-10-28
---

## Execution Boundary

* Task ID: employee-redeploy-20261028
* Scope: full plan attempted; only dependency-ready read-only backup permitted.
* Source: merged main `bb6df04cef68cc3694a97238d002c732c3406d81`.
* Branch: ops/employee-redeploy-20261028, initially clean; no existing PR.
* Plan: .copilot-tracking/plans/2026-10-28/employee-redeploy-plan.md
* Details: .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md
* Research: .copilot-tracking/research/2026-10-28/employee-redeploy-research.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-28/employee-redeploy-plan-critique.md
* Status: Blocked before build, push or cloud mutation. No redeploy claimed.

## P01-T01: Safe preservation

Backup complete, directory `/tmp/ama-employee-redeploy-20261028.nbVE6l`
(0700), JSON files0600, not committed. App safe projection retains complete
configuration/template/identity and exact existing image/env/registry/scale;
secret definitions contain only name/keyVaultUrl/identity, never values.
No `.env`, private data, secret values or listSecrets requested. Existing
noncredential configuration is captured externally, never committed.

| File | SHA256 |
|---|---|
| app-before.json | 3193c65c51640a465e792ea4bc546f7d7f105dff1acaa1292c7934e330c6d8f6 |
| revisions-before.json | 3bd9f22fadbf627dca44bbe6dbeba1c9b716680f434a81f1298441c186de61ec |
| acr-before.json | 9e76914c9b68fdbb2ab90bc3f87f171e961568301b53c582b450694090d720d3 |

Fresh independent GETs saved as app-after.json/acr-after.json and semantic
equality assertions passed, exit0; verification.json records sanitized results.
Old revision `ca-cutover-test-demo-api--0000006`; image
`crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:0769b52dddc5d6b350c74d6711ae53eda45d3e903ee27fac6b5a6c1d6b8b6e7e`.
Twenty-seven original env entries, one Key Vault reference, user-assigned
identity/registry selection, min0/max4 and Single mode all unchanged. Three AI
entries remain absent. No new revision or digest exists.

## P01-T01/P01-T02: Admission and cost failures

* `lslocks --noheadings --output PID,COMMAND,PATH` observed PID3869238,
  `python3`, holding `/tmp/ama-rpi-heavy.lock`; no wait/poll/interruption.
  Build NOT RUN, no image created or pushed.
* Read-only subscription ActualCost MonthToDate query API2025-03-01 failed429
  TooManyRequests, exit1. One alternative API2023-11-01 explicit
  2026-10-01..2026-10-28 query failed Unauthorized/RBACAccessDenied, exit1.
  No roles, logout/login or shared session changes. Required headroom remains
  unknown. No cloud writes or registry exception permitted.
* Original critique PC-001 also requires supported Single-mode rollback while
  preserving mode/traffic without another revision. Official docs consulted
  read-only; no compliant route established and no mode exception inferred.
* PC-002/004/005 corrections define positive readiness evidence, actual
  synthetic HTTP proof and concrete registry timeout/restoration bounds if a
  later separately admitted attempt proceeds. None was run or claimed here.

## P02: No rollout or rollback

No `az containerapp update`, revision activation/restart/mode/traffic mutation,
ACR update/rule/login, token request, Docker login/push or inference occurred.
No new revision/digest exists. Previous revision remains the rollback baseline.
No recovery action is necessary because no cloud mutation was attempted.
ACR final policy equals baseline: public Disabled, default Allow, IP/VNet
arrays empty, bypass None, exports disabled, admin false. It was never opened;
"unchanged" is the correct result, not a claimed restoration operation.

## Validation and Remaining Work

* Exact three AI values verified in runbook, #515 body, Bicep and model GET.
* Existing app/template/identity/registry/secret-reference/scale and ACR policy
  backup and full semantic equality verified, exit0.
* Local image/assets, new-revision health/startup/log checks NOT RUN:
  no new image/revision exists. Do not equate old revision health with redeploy.
* Full local publication gate NOT RUN / Blocked; foreign heavy-lock ownership
  prohibits queueing or polling/re-admission without a later coordination
  event. No passing receipt exists; no inherited exception from #515.
* Human/live/inference acceptance remains unchecked.

## Amendments, Divergences and Handoff

Immediately relevant current-state updates: actual foreign heavy-lock ownership
and denied financial evidence block affected dependent work. Conservative
critique corrections applied; original Revise verdict preserved, no repeat.
Implementation cannot satisfy full plan. Independent Review assessed the full
request against actual read-only/blocked execution, not deployment success.

## Pre-Review Reconciliation

* P01-T01 partial (backup complete, build blocked); P01/P01-T02 and
  P02/P02-T01/P02-T02 unmet, no runtime acceptance.
* P03-T01 complete: original independent Review Complete / Not accepted.
  P03-T02 local evidence commit authorized, full publication remains blocked.
  No completed runtime phase marker invented.
* Plan/details/state/changes agree on actual no-write boundary and blockers.
* Review readiness: ready only for independent assessment of blocked outcome,
  not conformant successful implementation or deployment acceptance.

## Independent Review and Publication Disposition

Original Review:
.copilot-tracking/reviews/logs/2026-10-28/employee-redeploy-review.md.
Execution Complete; outcome Not accepted. Three High, one Medium and one Low:
recovery to planning, financial evidence to research, unexecuted redeploy/
publication to later implementation, authenticated acceptance to distinct owner
follow-up. No findings closed by reimplementation or a repeated Review.
Review did not inspect external backup bytes due its own host boundary; parent
direct equality results above are retained as execution evidence, not upgraded
to independent Azure attestation.

RPI assessment finished, requested deployment still blocked. Automatic session
remains running at Follow-up with ranked evidence-grounded work in state.
Only the expressly requested local evidence commit is permitted now.
Full gate NOT RUN / Blocked, no verified receipt; no push or PR. This is not a
local-gate failure receipt, deployment success or authorized gate exception.
No new revision/digest, hosted checks, authenticated assets or runtime logs
exist for this attempt; original employee and ACR configurations are unchanged.
