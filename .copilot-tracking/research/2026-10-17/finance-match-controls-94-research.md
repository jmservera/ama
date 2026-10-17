---
title: Finance match controls 94 research
description: Exact criterion audit of record-only finance
ms.date: 2026-10-17
---

## Research brief and parameters

Status: Complete. Research disposition: executed. Planning Readiness: Ready.
Task #94, parent #93 (hierarchy, not dependency). Output mode: audit.
Resolved evidence root: `.copilot-tracking/research/2026-10-17/`.
Focused posture selected by caller's exact bounded scope.

Questions: Does any product path pay? Are match exceptions line-level and unknown
inputs refused? Does preparer identity, including staff/OID aliases rather than
role alone, prevent approval? Audit helpers, API, screens and SQL transactions.
Preserve budgets, commitments and held record-only dispositions. No authority,
currency or banking invention, private data, paid AI or Azure actions.
Use tiny fictional fixtures and migrated src only. Research is read-only except
this evidence and session state.

## Extensions and participation

Repository instructions apply to all inputs. Selected rpi-research and mandatory
subsequent RPI phase skills; web skills skipped unless web edits prove necessary.
Company Finance specialist skipped: executable enforcement, not fictional policy.
Inline investigation avoids splitting one continuous finance trace. No new
human decisions needed: caller provided criteria, exclusions and full execution.
Original case study and memory read; addendum and index routed by relevant
sections. Exact PRD/BRD references and component guides pending.

## Prior knowledge gate and direction controls

Issue says delivered record-only and unknown inputs block match; verify rather
than assume. No worktree changes existed. Latest origin/main is bab4bf3.
Explicit dependency endpoint returns empty; #90 and #84 both have no declared
dependencies. Related vocabulary is not a dependency. Inspect actual shared
Store/server surfaces before editing and flag overlap.

## Research cycle 1

### Wider

Executed inline: exact issue and parent, backlog #90/#84, source requirements,
component guides and finance entry-point discovery. Reflection: record-only
paths exist; exact acceptance is not yet proven by role-based tests.

### Deeper

Executed after Wider reflection: traced finance helpers, Store, SQL locking/save,
API dispatch and finance screens. Baseline 29 finance/signoff tests pass.
Reflection: all-invoice exceptions use null line IDs; different_person compares
email alone. SQL staff cache is not refreshed by ordinary case synchronization.
Finance disposition trusts the earlier Matched status rather than current totals.

### Contrarian

Executed after Deeper reflection: challenged same-role different humans versus
one human with different staff/email records and identical OID; checked legacy
preparer resolution, concurrent approval/acceptance, failed save/audit behavior,
and requirement numbering. SQL save already checks rowversions and uses a
cross-process writer transaction; reuse rather than replace it. Its generic
failure path can flush a staged success audit on lock exit unless finance drops
pending writes explicitly. Existing named-staff validation in change_provenance
can be reused; final transaction-time finance validation needs one small shared
SqlStore hook. No server or screen change needed: existing error and integer
line rendering already fit.

### Parent synthesis and re-entry

Accept demonstrated static gaps C2-C5 for failing-first verification during
Implement. Reject payment integration, expanded finance policy, currency models
and unrelated signoffs/procurement changes. One focused cycle covers all questions;
no further discovery justified. This audit explicitly prepares Plan.

## Evidence log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| W1 | Three exact criteria; existing record-only status; no dependencies; parent 93 | https://github.com/jmservera/ama/issues/94 (retrieved 2026-10-17) | High |
| W2 | Procurement 90 and signoffs 84 are concurrent scopes, no explicit dependency | https://github.com/jmservera/ama/issues/90 and https://github.com/jmservera/ama/issues/84 (retrieved 2026-10-17) | High |
| C1 | PRD FR-018 and AC-021/042 specify record-only finance and line exceptions | docs/prds/zava-forward-retrofit-programme-demonstrator.md:853,1467,1488 | High |
| C2 | Aggregate match exceptions have line=None; first matching commitment selected | src/core/src/zava_forward/core/finance.py:32-68 | High |
| C3 | No-self-approval helper compares email only, not stable staff/OID identity | src/core/src/zava_forward/core/controls.py:36-38 | High |
| C4 | Finance checks request role only and accepts cached Matched status | src/core/src/zava_forward/core/finance.py:75-83,165-180 | High |
| C5 | SQL transaction/rowversion machinery exists; staff cache and generic-error pending audit need scoped handling | src/core/src/zava_forward/core/sqlstore.py:437-441,501-603 | High |
| C6 | Fresh registered actor and transaction-time validation prior art | src/core/src/zava_forward/core/change_provenance.py:15-44 | High |
| C7 | API dispatch and existing line renderer need no modification | src/api/src/zava_forward/api/server.py:873-875; src/api/src/zava_forward/api/web/panels.js:28-34 | High |
| C8 | Baseline tests exercise role denial, but lack same-role preparer and OID alias controls | src/core/tests/test_finance_signoffs.py:65-88 | High |

## Source conflict and backlog disposition

Current BRD FR-018 is named human handoff acceptance (line 1428) and RULE-003
is hazard-service ownership (line 1393), not finance. Issue references are stale
numbering; preserve that contradiction explicitly. PRD FR-018 and exact issue
criteria govern this bounded task, without rewriting approved source documents.
PRD acceptance is broader than these three issue criteria; do not claim complete
AC-021/042 or company authority. #90 owns procurement/capacity; #84 owns technical
signoffs. Only actual potential shared overlap is SqlStore.save; retain their
behavior and flag the isolated validation hook. No dependency invented.

## Decisions, risks and next action

Questions answered: product never executes payment (C1/C4/C7); line-only and
identity criteria have gaps (C2/C3); stale matching/fresh permissions and rollback
are tightly coupled write controls (C4-C6). Plan failing-first tests then minimal
finance-owned fixes, one SQL save hook, focused JSON/SQLite/HTTP coverage and
local SQL Server if available. Existing migration lint/type exemptions remain.
No private data or external authority consulted. Source references are code/docs
and GitHub issue metadata only; no regulatory currentness claim.

Self-check: all three ordered waves, findings, alternatives (retain unchanged
versus scoped correction), rejected scope, provenance, readiness and next owner
recorded. No source implementation edits occurred during Research.
