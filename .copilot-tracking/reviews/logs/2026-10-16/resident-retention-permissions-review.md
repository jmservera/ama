---
title: Resident retention and permissions review
description: Single post-implementation acceptance review for the issue 86 follow-up
ms.date: 2026-10-16
---

## Scope and Evidence

* Task: issue-86-resident-retention-permissions.
* Plan: .copilot-tracking/plans/2026-10-16/resident-retention-permissions-plan.md.
* Details: .copilot-tracking/details/2026-10-16/resident-retention-permissions-phase-details.md.
* Critique: .copilot-tracking/plans/2026-10-16/resident-retention-permissions-critique.md.
* Research: .copilot-tracking/research/2026-10-16/resident-retention-permissions-research.md.
* Changes: .copilot-tracking/changes/2026-10-16/resident-retention-permissions-changes.md.

## Opening Review State

Single review, owned inline: the complete relevant policy diff fits a direct
read, so no additional worker or repeated review is justified.
Source implementation, local checks and real Azure SQL assertions complete;
documentation updated. Authorized resource-group deletion is still finishing.
Git delivery follows review and cleanup. Review writes only this record;
no source changes or repeated critique.

## Execution Status

Execution: Complete. Exactly one post-implementation Review.
Source implementation and SQL verification pass. Whole-task cleanup confirmation
has a platform authorization blocker, recorded as RV-004, not assumed successful.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Shared calendar schedule; earliest contact marker; legal-hold-aware retention approval; JSON/SQLite boundary/purge tests | Reconciled |
| P01-T02 | Registered human writer gate, legacy endpoint, separate view set, detached resident subtrees, contractor flags and record-only form gating | Reconciled |
| P01-T03 | Final publication 418 core, 537 API, 70 agents; exact-field tests; local HTTP; Ruff/format/mypy; Node rendering | Reconciled |
| P02-T01 | Real Azure SQL Basic database; new MssqlStore connections preserve decisions and purge; intact audit; ledger off | Reconciled |
| P02-T02 | SQL/apps/storage/AI/monitoring observed removed; final operation polling and existence read became forbidden after group-scoped access disappeared; filtered group list empty | Final independent confirmation blocked, RV-004 |
| P02-T03 | Documentation/log and artifacts committed, draft PR 326 open; final review/evidence commit follows | Parent delivery closeout |

## Implementation-Time Updates and Critique

PC-001 inventory includes reset of legacy answer and service representative refs,
retains complaints/general contact evidence and minimal marker; new legacy audit
notes removed. PC-002 includes safe-contact history and rejects unusable dates.
PC-003 preserves authorized resident notes independently of unrelated
vulnerability permissions. PC-004 applies expiry to direct representative
disclosure reliance. PC-005 explicitly limits deletion evidence to current
payload and records actual ledger mode. PC-006's invented tempfile restriction
was rejected, not silently converted into a requirement.

Ordinary coupled corrections preserve the existing manager complaint/redress
route; managers still cannot record resident decisions or authority. UI follows
that same boundary. Partial content fixtures without resident objects remain
Unknown rather than crashing. No unresolved significant owner decision, no
material scope expansion and no premature activation of operational controls.

Origin/main advanced with accepted PRs 321 and 324 during execution. A normal
non-rewriting merge into this topic resolved only an append-only log conflict,
preserving both main entries before this task's entry. The actual resident
policy, projection and SQL implementation remained unchanged; full integrated
core/API suites and type/lint checks passed. This is integration of accepted
main, not a new policy decision, a repeated critique or a second Review.

## Findings and Residual Work

No in-scope implementation defect identified in the assessed source/validation
boundary. Existing operational gaps remain distinct follow-ups:

### RV-001 [Medium]: Reconcile real resident identity and earliest contact evidence

The case schema has no universal resident identifier. A missing/invalid contact
origin remains Unknown, and earliest recorded contact must be preserved across
cases by the owning data flow, not inferred by name/address.
Destination: distinct rpi-research follow-up before real-data activation.

### RV-002 [Medium]: Approve operational history/backup erasure design

Current-payload removal and work/disclosure expiry are implemented. Existing
immutable audit content, backups and history are not erased; deletion remains
manager-reviewed, not a configured automatic purge service.
Destination: distinct rpi-plan follow-up with the human data/control owner.
No historical-erasure success or legal compliance is claimed.

### RV-003 [Low]: Complete named human and accessible resident acceptance

Named operational delegates, formal complaints integration and resident
without-detriment acceptance remain issue 86 work. Synthetic tests, a real
SQL engine and an intact audit chain cannot satisfy human acceptance.
Destination: owner-led acceptance follow-up; no issue closure.

### RV-004 [Medium]: Final Azure teardown confirmation lost its read authority

`az group delete --name ama --yes` was accepted and removed the observed SQL,
apps, storage, AI and monitoring resources. Last authorized resource inventory
contained only cae-forward-test (Consumption/ScheduledForDelete), VNet and
two NSGs. The command's subscription operation-result poll subsequently returned
AuthorizationFailed. Direct group show/exists/resource inventory retries are now
forbidden; the authorized filtered group list returns empty.

That is consistent with group-scoped RBAC disappearing during deletion, but
does not independently prove the final group/managed-environment absence.
No alternate identity, permission escalation or claimed zero-cost guarantee.
Destination: owner/platform follow-up with subscription-scoped read authority:
verify ama and its managed environment are absent, remove any remaining resources.
This blocks the whole-task cleanup completion claim, not the verified source fix.

## Validation Evidence

* New tests failed on the original source: manager mutation wrongly succeeded
  and first-contact retention helper was absent.
* Final full core 401 run/1 Azure opt-in skip; API 517 run/99 existing opt-in
  skips; agents 70 passed. Later exact-field and UI changes covered by targeted
  resident 30 run/1 skip, HTTP/role 13 and Node render checks.
* Core/API Ruff, format and mypy passed. Diff whitespace check passed.
* Current-main integration: 409 core run/1 opt-in skip (162.630 seconds);
  534 API run/103 existing opt-in skips (291.507 seconds), all passed.
  Ruff/format passed; mypy passed for 82 core and 42 API source files.
* Synthetic real Azure SQL: 1 test passed in 10.889 seconds; actual ledger off.
  Verified per-measure Proceed/Hold, manager denial, coordinator view, first
  contact anniversary, disclosure expiry, new-connection persistence and purge,
  marker survival and audit integrity.
* Live model, real residents, hosted CI and browser/human acceptance not run.

## Outcome

Outcome: Residual work. No in-scope source defect identified; local and real SQL
engineering evidence is accepted within its stated boundary. RV-004 blocks
verified final cleanup. RV-001 through RV-003 are existing operational
follow-ups outside this engineering slice, not invented approvals.
No second Review or implementation correction loop is requested. Issue 86 stays open.

## Post-review Publication Integration Evidence

Main subsequently accepted PR 325. Publication required an ordinary merge,
not a new lifecycle task or repeated Review. The source conflict combined its
queue privacy projection with the reviewed stricter contractor status/flag
contract. A generic documentation-session filename collision retained both
records. Resident retention/write persistence and SQL driver unchanged.
Final combined core 418/1 skip and API 537/103 skips passed; Ruff/format and
mypy (84 core, 43 API files) passed. This records integration evidence only,
not another Review or a new Azure run. RV-004 remains open.
