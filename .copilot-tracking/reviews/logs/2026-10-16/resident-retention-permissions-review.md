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

Execution: Partial, assessment in progress pending final cleanup evidence.
No conclusion yet about the whole task's delivery completion.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Shared calendar schedule; earliest contact marker; legal-hold-aware retention approval; JSON/SQLite boundary/purge tests | Reconciled |
| P01-T02 | Registered human writer gate, legacy endpoint, separate view set, detached resident subtrees, contractor flags and record-only form gating | Reconciled |
| P01-T03 | 401 core, 517 API, 70 agents; exact-field tests; local HTTP; Ruff/format/mypy; Node rendering | Reconciled |
| P02-T01 | Real Azure SQL Basic database; new MssqlStore connections preserve decisions and purge; intact audit; ledger off | Reconciled |
| P02-T02 | SQL/apps/storage/AI/monitoring removed; consumption environment and free network resources awaiting Azure deletion | In progress, not claimed complete |
| P02-T03 | Core/API documentation and reference index/log updated; git commit/push/PR follow review | Delivery pending |

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

## Validation Evidence

* New tests failed on the original source: manager mutation wrongly succeeded
  and first-contact retention helper was absent.
* Final full core 401 run/1 Azure opt-in skip; API 517 run/99 existing opt-in
  skips; agents 70 passed. Later exact-field and UI changes covered by targeted
  resident 30 run/1 skip, HTTP/role 13 and Node render checks.
* Core/API Ruff, format and mypy passed. Diff whitespace check passed.
* Synthetic real Azure SQL: 1 test passed in 10.889 seconds; actual ledger off.
  Verified per-measure Proceed/Hold, manager denial, coordinator view, first
  contact anniversary, disclosure expiry, new-connection persistence and purge,
  marker survival and audit integrity.
* Live model, real residents, hosted CI and browser/human acceptance not run.

## Outcome

Pending final cleanup evidence. Residual operational follow-ups do not convert
owner exercise policy into legal certification or close issue 86.
