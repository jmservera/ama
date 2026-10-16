---
title: Deployed src proof implementation review
description: Single evidence-based review for issues 200 and 201
ms.date: 2026-10-16
---

## Scope and Evidence

* Task ID: issues-200-201-deployed-src-proof.
* Review date: 2026-10-16.
* Review scope: full requested bounded deployment proof, not issue acceptance.
* Assessed boundary: private deployment, synthetic SQL state, ingress denial,
  restart, safety constraints, evidence and offline regression coverage.
* Plan: .copilot-tracking/plans/2026-10-16/deployed-src-proof-plan.md.
* Details: .copilot-tracking/details/2026-10-16/deployed-src-proof-phase-details.md.
* Critique: .copilot-tracking/reviews/2026-10-16/deployed-src-proof-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-16/deployed-src-proof-changes.md.
* Research: .copilot-tracking/research/2026-10-16/deployed-src-proof-research.md.
* Evidence: docs/architecture/cutover-evidence-pack.md and
  docs/architecture/cutover-azure-evidence.json; staged infra diff and tests.

## Opening Review State

* Interpreted goal: assess actual private proof against confirmed owner limits
  without converting tenant blockers or synthetic results into issue acceptance.
* Scope: P01-P03 implementation and review-ready evidence; publication follows.
* Evidence readiness: all implementation markers reconciled; test, deployment,
  execution, image and restart evidence available. No owner sign-off supplied.
* Acceptance basis: plan requirements, per-check statuses, PC-001 through PC-006
  dispositions and original user constraints.
* First comparison boundary: template/runner behavior versus actual job evidence,
  then plan-to-change reconciliation and residual routing.
* Read-only boundaries: Review writes only this record; no source/plan correction,
  cloud mutation, tenant changes, dataset access or repeat Review.
* Initial blockers: authorized HTTP token acquisition and human staff
  initialization lack tenant/owner prerequisites; other checks remain assessable.

## Execution Status

* Execution status: Complete.
* Review evidence: one full comparison of reconciled artifacts, staged source
  and recorded Azure execution; offline infra rerun passed 117 tests.
  No review subagents, repeat Review or new Azure writes.

## Plan-to-Change Reconciliation

| Scope | Changes and current reconciliation | Assessment |
| --- | --- | --- |
| P01-T01 | Effective access is development AND explicit switch; matrix preserves production rejection and dev defaults | Reconciled |
| P01-T02 | Metadata/sentinel guard precedes Store; fictional nonempty fixture; MI separation and ten runner tests | Reconciled |
| P01-T03 | Opt-in bearer mode, nonempty audience guard, no delegated token store; existing browser mode preserved | Reconciled |
| P02-T01 | ACR dba/dbb before isolation; explicit digest wrapper; private environment-first bootstrap | Reconciled |
| P02-T02 | Dedicated initializer, Graph-free contained users; successful one-case/zero-staff initialization | Reconciled |
| P02-T03 | Actual 200/401 private probes, replaced replicas, seedless API-MI state reload; tenant blockers explicit | Reconciled |
| P03-T01/P03-T02 | Current pack/JSON/index/log, scoped tests, redaction/reference checks and review-ready handoff | Reconciled; publication follows |

## Completed Work Assessment

* infra/main.bicep and infra/modules/containerapps.bicep implement the private
  switch and environment-only stage without changing default browser behavior.
  Workload/auth conditions and conditional outputs align; guard prerequisites
  fail closed. Deployment success corroborates compiled-policy tests.
* infra/scripts/private-cutover-proof.py refuses unknown application tables
  before Store construction, checks proof ownership, selects explicit MI,
  validates contained SIDs and rejects unexpected roles/names. Errors emit
  explicit Failed/type without raw exception payloads.
* Actual SQL initialization and separate API-MI reads distinguish privileged
  setup from runtime grants. Post-restart proof checks the same application
  case/marker, zero staff, unavailable seed and no reseeding.
* Private origin resolves to 10.40.0.184; SQL resolves to 10.40.4.25. Health is
  200; anonymous, malformed bearer and forged principal probes are 401.
  Both serving replicas were replaced, not merely a restart command accepted.
* docs/architecture/cutover-azure-evidence.json keeps historical failures
  distinct from current deployment Succeeded and aggregate Partially passed.
  Owner checklist is unchecked; historical log entries and protected paths
  remain unchanged. Current inventory retains three budgets and 87 resources.

## Implementation-Time Plan and Detail Update Assessment

| Update | Trigger and rationale | Reconciliation and decision boundary |
| --- | --- | --- |
| Ledger alert schema | Workload rollout rejected obsolete table/columns; management-plane table metadata supplied actual schema | Both queries and compiled regression updated; no query-validation bypass; directly coupled deployment blocker |
| Assistant allowlist | First post-restart instrument rejected five legitimate startup tables | Metadata-only diagnosis, installed-DDL allowlist and unknown-table regression; no private case/staff diagnostic read |
| Hashed source-command instrument | Registry already isolated; no default private repair-build route | Explicit job command on same immutable image/API MI; hash equals tracked source; no network reopening or image-provenance substitution |
| Bounded partial result | MI HTTP token endpoint 400; Graph lookup denied; no private roster | Plan follow-ups, changes and canonical evidence preserve user intent; no fabricated tenant roles or staff |

No new owner decision or second critique was required: these corrections
implement the confirmed private-network and honest-blocker direction. The
proof-image/source difference is disclosed rather than hidden.

## Critique and Material Revision Assessment

PC-001 through PC-006 each have direct plan dispositions and implementation
evidence: environment-first ordering; pre-Store metadata guard; administrator
versus contained-client identity separation; nonempty application persistence;
negative bearer/proxy probes; builds before registry isolation. The corrected
instrument uses an explicitly documented management-plane command, not an
unevidenced repair build. Valid-token acceptance is not inferred from negative
tests. No incompatible critique recommendation or unaccepted decision remains.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate execution | Owner or next action |
| --- | --- | --- |
| Authorized HTTP | Existing application cannot issue the requested MI token; no approved API role prerequisites | Tenant/API owner, RV-001 |
| Human staff initialization | No approved private roster or Graph rights; MI is not staff | Owner/tenant administrator, RV-002 |
| Functional workers and owner cut-over gates | CLI/image checks and a fictional fixture do not prove product/private-data acceptance | Product/operator/owner, RV-003 |

These remain distinct follow-ups, not newly added implementation tasks.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Authorized HTTP remains unproved

* Scope: P02-T03 and authorized-HTTP follow-up.
* Evidence: canonical JSON smoke.authorized_http records token endpoint HTTP
  400; valid_token_issuer_audience_acceptance is Not run.
* Impact: 401 denials and authenticated SQL cannot establish valid-token HTTP
  acceptance or staff-authorized behavior.
* Destination: distinct tenant/API prerequisite follow-up, then in-VNet proof.
* Next action: tenant owner confirms approved audience/role configuration and
  grants only justified prerequisites; repeat the positive path privately
  without token publication or mapping an MI to a human.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Human staff initialization needs owner and tenant inputs

* Scope: plan human-staff follow-up.
* Evidence: Graph lookup returned Insufficient privileges; fixture has zero
  staff; no approved private roster or workbench registration supplied.
* Impact: workbench staff initialization and human-authorized API acceptance
  remain Blocked independently of SQL/network success.
* Destination: distinct owner/tenant initialization follow-up.
* Next action: obtain approved roster and tenant-authorized initialization path;
  execute inside the AMA VNet, keeping private inputs out of Git.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Worker and owner acceptance remains separate

* Scope: plan remaining cut-over follow-up.
* Evidence: agents app is scale-to-zero skeleton; orchestrator/importer
  executions prove CLI entry points only; owner checklist stays unchecked.
* Impact: no four-functional-worker, continuing-stock, backup or cut-over
  approval claim is justified by this infrastructure exercise.
* Destination: distinct functional acceptance and owner gate follow-up.
* Next action: product/operator owners define and obtain real functional and
  private-data evidence; owner retains the approval decision.

## Defects and Routed Findings

No implementation defect was identified in the assessed boundary.

| Finding | Destination | Reason |
| --- | --- | --- |
| RV-001 | Tenant/API owner follow-up | External prerequisite, not authority to weaken authentication |
| RV-002 | Owner/tenant staff follow-up | Required private and tenant inputs absent |
| RV-003 | Product/operator and owner acceptance follow-up | Outside synthetic infrastructure acceptance |

Later follow-up work does not require repeating this Review.

## Blockers and Remaining Work

Tenant token issuance and approved human initialization block only those
checks, not review or publication. No SQL/network deployment blocker remains.
Remaining delivery: parent commits, pushes and opens PR with bounded outcomes
and non-closing issue references. No resource cleanup or owner sign-off is
implied.

## Validation Evidence

| Validation | Status | Boundary |
| --- | --- | --- |
| REQUIRE_AZ_BICEP=1 venv/bin/python -m unittest discover -s infra/tests -q | Passed | 117 tests, 21.082 seconds in review; ten runner tests included |
| All infra Bicep build/lint and scoped Ruff check/format | Passed | Recorded implementation commands; not replaced by mocks |
| Reference audit --write and check | Passed | 130 parity rows, 1464 reference locations, no missing destinations |
| Staged identifier/token, Markdown links and owner/protected-path assertions | Passed | Known current subscription/tenant/identity values compared without printing them; RPI links use workspace convention |
| Runner SHA-256 | Passed | 0560f367cf36fa7dd0e850040c55463b712b781a465d1ebd5f4e8de6406cd7e4 equals recorded deployed command |
| Azure private bootstrap and corrected rollout | Passed | Succeeded 14:03:51 and 14:17:06 UTC; no Delete |
| In-VNet initialization, negative HTTP and restart proof | Passed | Actual execution names/outputs in canonical evidence |
| Original post-restart SQL instrument | Failed | Allowlist mismatch, retained honestly; distinct corrected execution Succeeded 14:22:48 |
| Authorized HTTP / human staff | Blocked | Token 400 / absent approved tenant and private inputs |
| Functional workers, live inference, private-data acceptance, owner sign-off | Not run | Not supplied or authorized by bounded proof |
| Full unchanged workload source suites and measured coverage | Not run | No source package changes; no claim of new coverage |

## Outcome

* Outcome: Residual work.
* Rationale: bounded private infrastructure proof is supported, with justified
  instrument/deployment corrections. Overall requested smoke is only partially
  passed and issues are not accepted as complete. RV-001 through RV-003 remain
  openly routed; no conformant full-acceptance outcome is claimed.

## Closeout Routing Record

| Finding class | Destination | Next owner |
| --- | --- | --- |
| Implementation defect | None identified | None |
| Unaccepted decision gap | None identified | None |
| New research gap | None requiring review-stage discovery | None |
| Residual work | RV-001, RV-002, RV-003 distinct follow-ups | Tenant/API, owner and product/operator |

* Review execution: Complete; outcome: Residual work.
* Return to explicit full-delivery parent for commit/push/PR.
* No second Review or follow-up implementation in this task.
