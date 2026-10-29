---
title: SQL roster chat revocation phase details
description: Task-level evidence and completion expectations
ms.date: 2026-10-29
---

Task `157-chat-sql-roster`; parent plan:
`.copilot-tracking/plans/2026-10-29/chat-sql-roster-157-plan.md`.
Research C1-C8 is adequate; no additional research or user decision required.

<!-- rpi:phase id=P01 -->
## P01: Correct resolver and regression contract

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add authoritative SQL actor lookup

Targets: `src/core/src/zava_forward/core/chat_isolation.py:current_user`.
Prior art: `regulatory_chat.py:admit`, `assistants.py:authorize`.
Use `hasattr(store, "db")`, `store.dblock`, bound email parameter and JSON row
body; missing row stays None. Keep verified Entra path before roster lookup.
Raise existing `ChatForbidden` for denied roles and disabled/inactive roster.
Existing panel reads occur at dispatch and after model result/failure; reuse.
Completion: no cache refresh, no panel duplicate lookup, no error-swallowing.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Cover stale-cache revocation and document behavior

Depends on P01-T01 for green results, but write tests first for red evidence.
Use `test_sqlstore.seed`, temporary SQL store, synthetic privacy refs and one
case-backed thread. Separate SQLite writer commits before returning model text.
Use valid answer/citation canary to distinguish a real release from abstention.
Compare both cache views before/after mutation. Dispatch denial means no user
message/model call; completion denial may retain question but no assistant
message; `chat.turn` audit says access-rejected. Allowed role change emits only
WITHHELD. Stable actor emits cited answer. No network or private datasets.
Amend final SQL history role switch to persist new actor before asking.
Document dispatch/completion lookup and local-evidence limitations in core README.

<!-- rpi:phase id=P02 -->
## P02: Validate and independently review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Demonstrate red/green and run focused checks

Depends on P01. Red: execute new test class before resolver edit. Green:
`test_chat_panel`, `test_chatthreads`, `test_chat_privacy`, `test_chat_memory`,
`test_chat_isolation`, `test_regulatory_chat` and relevant API panel module.
Use `/tmp/mv` and the plan's cwd/PYTHONPATH, no package install unless missing
dependency failure. Ruff uses core pyproject; migrated isolation is intentionally
format-excluded. Record commands, counts, skips and failures without concealing
the original red or treating SQL Server skips as passes.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Record one independent Review and commit locally

Depends on P02-T01. Fresh reviewer reads current plan/critique, changes and
targeted diff with validation evidence. Write only the dated review artifact.
Do not silently fix Review findings and repeat Review. Update state and all
markers before local commit. Resolve `gh api user` and set repo-local noreply
email for author/committer; include `Refs #157` and requested Copilot trailer.
No publication receipt, push, merge, issue change, az or manual rubric edit.

## Current Completion and Handoff

P01-T01/P01-T02 and P02-T01 complete. New stale-cache regression failed before
the fix (11 failures across four tests); current core focused set passed 146
tests, API panel passed 38 with one opt-in Chromium skip. Final core panel rerun
passed 22. Ruff check, configured format check (`--force-exclude` preserves the
existing isolation exclusion), targeted mypy and whitespace check passed.
The initial API selector collision and lint/type/format command failures are
retained in changes evidence. No source work or significant divergence remains.
P02-T02 independent Review executed once: Complete / Conformant, no findings;
its original artifact is
`.copilot-tracking/reviews/logs/2026-10-29/chat-sql-roster-157-review.md`.
The source-patch fingerprint still matches the reviewed boundary. P02-T02
completed with local implementation/evidence commit `83acf525`, including the
requested trailer and GitHub-resolved privacy-safe author/committer email.
All P01/P02 markers complete; final state reconciliation is evidence-only.
No source change after Review and no push, az or manual rubric edit.
