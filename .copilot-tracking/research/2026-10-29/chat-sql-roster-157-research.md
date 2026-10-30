<!-- markdownlint-disable-file -->
---
title: SQL roster chat revocation research
description: Focused evidence for issue 157 and PR 503
ms.date: 2026-10-29
---

## Research Brief

Resolve the employee chat actor from authoritative SQL staff records at dispatch
and completion, and reject revoked access without releasing or persisting an
answer. Audience: implementer and independent reviewer of PR #503, Refs #157.
Output mode: convergence, preparing planning. Posture: focused, selected from the
owner's named failure path and minimal-source-change constraint.

## Research Parameters and Direction Controls

* Source changes only in `src/`; dated RPI evidence in `.copilot-tracking/`.
* Reuse `feat/agent-chat-157`, already rebased; initial pull absorbed bot rubric
  commit `6989bbb5`. No push, Azure operations, or manual rubric edits.
* Validate SQLite changes without modifying cached staff; focused chat tests in
  `/tmp/mv`, Ruff check and Ruff format check.
* Questions: where is actor identity resolved; what authoritative lookup exists;
  what happens on row deletion/demotion; which tests preserve non-SQL behavior?
* Internal candidates: chat panel/isolation, SQL staff lookup, chat tests and
  component README. External candidates: none required for this internal fix.

## Extension Registry and Participation

Repository instructions and RPI skills selected for evidence, minimal changes,
and independent critique/review. Web skills skipped: backend-only.
Security audit agent skipped: owner requests repair of an identified finding,
not vulnerability discovery. Research inline: one tightly coupled code trace.
No interaction required: owner supplied scope, branch, environment and outcome.
Prior-knowledge gate: supplied finding is a hypothesis to verify against source;
history query found no relevant sessions in seven days.

## Research Cycle Log

Cycle 1 opening: Wider will trace the current actor/cache contract; Deeper will
inspect SQL lookup and regression fixtures; Contrarian will check non-roster,
unknown-role, missing-row and completion behavior.

Wider completed inline: panel dispatch and completion both call
`ChatIsolation.current_user`. Its roster branch reads cached dictionaries.
Reflection: repair that shared resolver, not the projection or SQL cache lifecycle.

Deeper completed inline: SQL staff records are JSON bodies keyed by lowercase
email; existing modules use parameterized lookup under `dblock`. `_sync` does
not reload populated staff even after the case sequence changes.
Reflection: direct reads at both existing call sites avoid dependence on cache
invalidation or restarting the store.

Contrarian completed inline: verified Entra principals intentionally use their
verified identity contract rather than a roster email. Preserve that branch and
the in-memory resolver. Missing rows must not fall through to cache. Existing
SQL history test changes only cache on its final switch, so it must persist that
switch to SQL under the new authority contract.
Reflection: no new cache API, global refresh, or identity redesign is warranted.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | `src/core/src/zava_forward/core/chat_panel.py:340`, `:473` | Existing dispatch/completion actor reads precede projection and release. |
| C2 | `src/core/src/zava_forward/core/chat_isolation.py:60` | Roster resolver currently trusts staff/data cache; verified Entra branch is separate. |
| C3 | `src/core/src/zava_forward/core/sqlstore.py:551` | `_sync` only loads staff when cache is empty and can return before checking staff. |
| C4 | `src/core/src/zava_forward/core/regulatory_chat.py:58` | Parameterized staff read under `dblock` is established local prior art. |
| C5 | `src/core/src/zava_forward/core/assistants.py:447` | Authoritative staff admission checks role and disabled/inactive flags. |
| C6 | `src/core/tests/test_chat_panel.py:272` | SQL history coverage needs SQL-authoritative final role switch. |
| C7 | `src/core/src/zava_forward/core/identity.py:89` | Verified Entra identity contract must remain unchanged. |
| C8 | `src/core/pyproject.toml:29` | Existing Ruff policy excludes migrated isolation formatting; panel tests are formatted. |

## Findings Mapped to Questions and Evidence

Actor resolution: C1/C2 confirm the finding. Lookup: C3/C4 justify a direct
parameterized SQL read in the roster branch, returning no actor on missing row.
Revocation: C5 supports denying disabled/inactive records as well as disallowed
roles. Regression: C6 requires tests whose SQL writes never mutate either cached
staff collection. Non-SQL and Entra paths remain unchanged (C2/C7).

## Alternatives and Decision State

Selected: repair shared `current_user` with existing SQL/dblock convention; keep
both panel call sites. Reject global `_sync` refresh because it changes unrelated
store behavior and still requires cache invalidation. Reject panel-only duplicate
lookup because it leaves a misleading shared resolver and duplicates authority.

## Open Questions, Risks, and Residual Uncertainty

No research blockers. SQLite proves local semantics, not SQL Server or actual
provider/operational acceptance. Completion read is not a new transaction-wide
revocation/answer-write atomicity guarantee. Preserve existing issue acceptance
gaps; do not close #157 or claim publication readiness.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready.
All three waves completed inline; no delegated lane or external evidence.
Questions answered by C1-C8, one selected approach, no unresolved decision.
Re-entry not required: further sources are redundant for this bounded fix.
