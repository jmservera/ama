---
title: AI metering Copilot threads phase details
description: Evidence and implementation completion expectations
ms.date: 2026-10-31
---

## P01: Source corrections and regressions

### P01-T01

C1/W1: mirror run's CURRENT branch in look_at; _request still updates actual
configuration while preserving root/attempt/capability/prompt/depth/retry.
Test exact shared-call and depth denial with a local text-document provider.
C2/W2: extract the existing timestamp/range check into report_period and reuse
in Consumption.report and server before ledger availability branching.

### P01-T02

C3-C6/W3-W5: permit reject-only orphan review-intent/review for legacy records;
keep unjoined output economics Unknown until original linkage repair.
For assistant rejection, supply original meter root to Consumption.review,
creating an ineligible link only if no matching output/root conflict exists.
On DispatchHeld append a closed review-unresolved marker directly using the
same SQL transaction. Persist financial_attribution unresolved in task history.
Do not mask SQL failures. Do not change approval/revision checks.
Reporting reads markers as-of, invalidates accepted denominator and counts
unresolved cohort reviews. Retain historical pre-withdrawal acceptance.

Critique refinements: legacy review_intent receives authoritative original root
and emits closed review-orphan(root, output, at) association only for missing
reject attribution. Existing v1 shapes remain valid. Orphan links validate
original-root repair, and reporting unions distinct pending/orphan output gaps.
Assistant review stages all checks from one bounded snapshot before link/review
writes; no second scan after link insertion. DispatchHeld fallback writes only
review-unresolved(root, output, action=reject, at, reason, revision), with the
authoritative task revision, and persists a task financial_attribution flag.
Markers are sticky, cohort-scoped, as-of-filtered and dominate equal-time
financial acceptance; ordinary later events never clear them. SQL insert/update
failures escape and roll back the entire authoritative transaction.

### P01-T03

Existing composed fixture already injects output-link failure for SQL/JSON and
legacy/priority paths: revise reject expectations and assert saved disposition,
incomplete report, then explicit original-link repair without duplicate edits.
Add pending failed-provider rejection and MAX_EVENTS overflow withdrawal tests.
Add isolated consumption tests for immutable existing output eligibility,
unresolved report handling and historical cutoff. Update core/API README and
existing knowledge-base synthesis/index/log concisely.

Test allocation (maximum eight additions; no removed or renamed methods):

* API document shared limits/standalone root/CURRENT restoration.
* API failed-provider pending rejection/ineligible link/no redispatch.
* API capacity-held accepted withdrawal/Unknown after recovery.
* API exact-capacity boundary/SQL rollback/authorisation/revision negatives.
* Core orphan rejection/cohort gaps/original link repair.
* Core assistant original-root repair/immutable conflicts/reject-only.
* Core unresolved cutoff/equal-time/restart/sticky semantics.
* Core unresolved cohort isolation/de-duplication.

Extend existing API legacy/priority SQL/JSON matrix and HTTP period method.

## P02: Validation, review and publication

### P02-T01

Install editable projects/tools using pip in an isolated session environment
after observed missing-import failure. Run focused modules first, then core/API
unittest discovery and each component's Ruff/check-format/mypy commands.
Keep expected opt-in skips qualified; no full gate per explicit user direction.
Completed: core 1638 tests / 206 opt-in skips; API 1443 / 320 opt-in skips.
Both configured Ruff/check-format/mypy pass; core 170 typed sources, API 124.
All eight added tests and existing modified methods ran in those suites.

### P02-T02

Fresh independent review of changed source/tests against all five threads,
plan and validation. One Review only; record findings and route remaining work
without claiming human/live approval or rerunning original adverse reviews.

### P02-T03

Resolve gh account locally for privacy-safe author/committer email and trailer.
Commit implementation and original dated evidence, then git push -u origin HEAD.
Reply to each original review comment with actual fix/regression evidence and
resolve its GraphQL thread only when satisfied. Verify remote head and threads.
No force, merge, issue close or hosted-gate approval claim.

Current handoff: P01 and P02-T01 complete, one independent P02-T02 Review next.
Publication remains pending; no source changes or material divergence after
the validated batch. No full-local-gate receipt or hosted/human approval.
