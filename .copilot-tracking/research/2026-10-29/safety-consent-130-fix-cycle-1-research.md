---
title: Issue 130 PR 509 fix cycle 1 research
description: Focused research into resident status and nomination identity regressions
ms.date: 2026-10-29
---

## Research Brief

Fix the two supplied Copilot findings in PR #509, Refs #130. Audience:
maintainers reviewing the local candidate. Output mode: convergence preparing
planning. Source edits stay in src/, tests outside packages. No Azure, push,
issue closure or hand-edit of latest.json. Run the requested core Ruff,
format, mypy and relevant unittest modules using /tmp/mv.

## Research Parameters

Focused posture, selected from the named source and supplied failure sequences.
One tightly coupled investigation is inline; no research delegation is needed.
Existing issue/PR and rebase artifacts are context, not fresh correctness evidence.
Initial questions: how does tenure affect status/ranking; how are nomination
identities allocated, persisted and deleted; what existing tests cover each?

## Direction Controls and Extensions

User explicitly requests the full loop and local commit without push.
Repository instructions, src/README.md, core guide and retention policy apply.
RPI phase skills selected; independent critique and Review will be separate.
Web/design, Azure and external regulatory research are not applicable.
No interaction is needed because scope and expected outcomes are explicit.

## Research Cycle Log

Cycle 1, Wider: inspected resident_decisions.py, Store._heuristic_priority,
core resident tests, shared JSON/SQLite test inheritance and API intake tests.
The branch matches open PR #509 and git pull --rebase was already up to date.
Prior-session lookup returned no matching records; dated rebase evidence
supplies context only.

Reflection: status is shared across ranking, SQL denormalization, insight and
prompt surfaces, so fix the common status computation rather than ranking.

Cycle 1, Deeper: traced resident_gate, resident_status, retention deletion,
nomination creation/correction and transactional replay. Existing deletion
already keeps a non-sensitive resident_retention_tombstone. Existing nomination
tests expect sequential NOM-1 and compare unrelated case state exactly.

Reflection: retain current IDs and API shape by adding a cumulative deleted
nomination count to that tombstone, not changing every new ID to UUID.

Cycle 1, Contrarian: evaluated bypassing tenure by copying/removing case
fields, dropping retention/authority checks, UUIDs, and an always-updated case
counter. Rejected field-copy bypass and weakened checks; a shared decision-only
gate preserves existing checks. UUIDs are established prior art but unnecessarily
change existing ID fixtures. Always-updated metadata is unnecessary when the
only nomination removal path is whole-ledger retention deletion. Repeated
deletions must preserve cumulative count, including deletion with no nominations.

Parent synthesis: both root causes are supported; no independent uncertainty
justifies research delegation. Focused scope is covered; further source search
would be redundant. No external/legal claim or source is needed.

## Findings and Evidence

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | src/core/src/zava_forward/core/resident_decisions.py:533-585 | Tenure returns before decision validation; resident_status uses that combined gate, incorrectly losing Accepted. |
| C2 | src/core/src/zava_forward/core/store.py:865-886 | Missing decision adds 20 and changes explanation; ai_tasks.py:58, insights.py:62/114 and sqlstore.py:543 also consume common status. |
| C3 | src/core/src/zava_forward/core/resident_decisions.py:620-705 | Deletion clears nomination_records; creation uses list length; correction only binds id/version, allowing deleted identities to match new intake. |
| C4 | src/core/src/zava_forward/core/controls.py:68-76 | next_id is length plus one; missing record already raises an explicit ValueError before version/mutation. |
| C5 | src/core/tests/test_resident_decisions.py:84-167,252-354,2666 | Shared test harness exercises JSON and SQLite with reopen/rollback assertions. Existing tenure test begins with accepted decisions but does not check heuristic/status. |
| C6 | src/api/tests/test_resident_api.py:142 | API tests rely on NOM-1. Retaining first-cycle IDs avoids unrelated interface changes. |
| C7 | src/core/src/zava_forward/core/resident_decisions.py:477-486,628-638 | Existing retention tombstone keeps counts without personal content and is not in RESIDENT_FIELDS. It can carry the cumulative deleted nomination count. |

## Alternatives and Decision State

Select a decision-only private gate used by resident_status and the existing
resident_gate after its tenure check. Preserve all retention, current scope,
resident review and representative authority checks. Select a cumulative
nomination count in the existing deletion tombstone, default zero for legacy
tombstones. Allocate count + retained list length + 1. No personal data survives.
Regression coverage must prove exact heuristic output/status equality while
case/scoped tenure holds remain, and stale correction refusal after deletion,
reopen and recreation across repeated retention cycles.

## Planning Readiness

Ready. Research disposition: executed. Both supplied failure sequences map to
source evidence and concrete shared JSON/SQLite regressions. No source edits
were performed in Research. No unresolved planning decision or research blocker.
