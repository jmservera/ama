---
title: Setup Entra expiry issue 358 implementation plan
description: Bounded reassessment of already-delivered safeguards and residual acceptance
ms.date: 2026-10-30
---

## Task Metadata

Task ID: 358. Slug: setup-entra-expiry-358. Date: 2026-10-30.
Planning status: Ready for bounded implementation; critique disposition complete.
Details: .copilot-tracking/details/2026-10-30/setup-entra-expiry-358-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-30/setup-entra-expiry-358-plan-critique.md.

## Executive Summary

Verify the already-merged expiry/preservation regressions and legacy delegation,
then add a dated runbook acceptance reassessment. No source defect or missing
regression was found; do not introduce redundant production/test changes.
The originally populated deployed-app/full-setup preservation criterion remains
unmet, not replaced by the earlier temporary synthetic exercise or this run.

### What You May Not Know

#374 and #417 already delivered the bounded implementation/evidence. This
task cannot satisfy the remaining live criterion under the user's no-Azure,
no-credentials boundary. Local failures will be recorded without unrelated fixes.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review in order with dated artifacts.
* Use supplied clean topic branch and base; commit locally with coauthor trailer.
* Refs #358 only; no push, PR, Azure, deployment, sign-in or credential access.
* Run requested API tests, Ruff lint/format and mypy; heavy work uses
  `flock -w 600 /tmp/ama-rpi-heavy.lock`.
* Preserve source under src, tests outside packages; no uv or web changes.

## Goals

* Establish current local evidence for each existing safeguard.
* State exact proven/unproven issue criteria without altering original reviews.

## Scope and Non-Goals

In scope: one dated paragraph/acceptance table in `infra/README.md`, current
tracking artifacts, focused infra tests and caller-requested API checks.
Non-goals: source refactor, duplicate tests, live operations, new helper,
credential files, issue status changes, remote publication or acceptance.

## Functional Requirements

* FR1: retain frozen-clock generated/legacy expired/equal-now/missing/future
  coverage and the seven existing behavioral mutations.
* FR2: retain KV URL/identity and app/token-store reference checks.
* FR3: retain the delegating `initialize-api-auth.py` main.
* FR4: distinguish historical synthetic component proof from missing original
  deployed-app/full-setup proof in current documentation.

## Non-Functional Requirements

No source or tests removed or added (maximum zero additions); canonical
production ownership remains `infra/scripts`, regression ownership remains
`infra/tests` outside packages. Generated targets: none.
Existing behavioral tests provide semantic/mutation coverage, not just text
matching. Use a run-owned external pip environment only after missing-tool/
dependency results. Record commands, exits, skips and limitations.
Human/hosted approval remains unperformed. No full receipt or publication claim.

## Acceptance Criteria

| ID | Criterion | Expected disposition |
| --- | --- | --- |
| AC1 | Stored expired credential regression detects bypass of generated and legacy expiry guards | Already implemented; prove by existing test and mutation execution |
| AC2 | Actual nonproduction preservation of originally populated app KV/token-store references through setup | Unmet/blocked: caller prohibits required live access |
| AC3 | Conflict with #352 resolved while retaining delegating legacy main | Already merged; confirm delegation test and lineage |
| AC4 | Current scoped documentation and dated RPI records are consistent and locally committed | Prove within this bounded loop |

## Sources

.copilot-tracking/research/2026-10-30/setup-entra-expiry-358-research.md,
C1-C9/W1-W3; current issue comments and current runbook.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve implementation and refresh acceptance evidence

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Run existing local regression and requested project checks

Dependencies: critique disposition. Execute `test_setup_entra` (including
mutation suite) and `test_initialize_api_auth`; confirm the existing legacy CLI
test in setup tests. Run API command from the user, Ruff check/format and mypy.
Use captured external logs; never invoke setup CLI against Azure.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Document current acceptance and implementation disposition

Dependencies: P01-T01 results. Add dated current boundary in infra runbook;
write changes evidence and reconcile plan/details/state. Preserve prior
paragraphs, tests, production files and historical RPI artifacts byte-for-byte.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Independent Review and local handoff

Dependencies: P01-T02. One independent post-implementation Review, route
findings without a repeat loop. Commit bounded candidate locally with trailer.
Attempt the repository's full local gate after the commit, with external
output; its built-in acquisition of the exact shared lock avoids double-lock
deadlock. Final receipt verification against current main/publication and
exact-head approval remain coordinator-owned; no push or PR.
Completion evidence: the one independent Review is Complete / Residual work;
the original candidate and evidence are locally committed as
`097354d9e6a6738aab1ff5683d477cde59aaee51`. This administrative reconciliation
does not change that Review or resolve AC2. The postcommit gate is a separate
validation control after the final reconciliation commit, not issue acceptance
or a prerequisite to recording the already-observed local commit.

## Dependencies

External pip environment, available heavy lock admission, local Python 3.12.
Live AC2 has no safe substitute and is excluded from bounded phase completion.

## Critique Disposition

Exactly one critique executed: Complete / Revise, one Medium finding PC-001.
Disposition: rejected as inapplicable to this parent execution. The critique
asserts a project-only/temporary-file prohibition absent from the caller and
parent execution context. The caller explicitly names
`/tmp/ama-rpi-heavy.lock`; developer context explicitly provides the external
session files directory. Preserve that exact shared lock, do not substitute a
project-local lock. Run-owned environment/log root:
`/home/azureuser/.copilot/session-state/ff88c0b4-017d-4da1-9a9a-a3ea3c2615fd/files/issue-358`.
No secret or credential file is accessed there. This is a direct evidence-based
disposition, not a change to the original critique or another critique run.

## Follow-Up Items

* FU1: authorized populated existing-app/full-setup preservation evidence;
  operator/coordinator owns a separately scoped live plan. Outside allowed run.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-30/setup-entra-expiry-358-changes.md.
Bounded phase complete. AC2 remains blocked regardless of phase checks.
Final external full-gate output root:
`/home/azureuser/.copilot/session-state/ff88c0b4-017d-4da1-9a9a-a3ea3c2615fd/files/issue-358/final-full-gate`.
Gate result is intentionally external so recording it does not invalidate
the committed candidate. No gate success is claimed in this pre-gate snapshot.
