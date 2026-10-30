---
title: Chat widget 550 Copilot findings phase details
description: Implementation and evidence boundaries for four corrections
ms.date: 2026-10-29
---

Task 550-copilot-fixes; parent 550-rebase. No initial blockers.
Current state: P01/P02/P03 complete upon the containing local commit.

<!-- rpi:phase id=P01 -->
## P01: Correct and regress

<!-- rpi:task id=P01-T01 -->
### P01-T01: Four corrections

Use research C1-C7. CSS tier 1100 and explicit close hover. Before message
append measure bottom distance <=1 and reject following if the log contains
activeElement. install opener/decorate in one !widget branch.
Extend existing Node DOM with scroll geometry as needed. Cover old history,
focused history at bottom, following and repeated install toggle. Add real
browser assertions using the current apps: computed contrast >=4.5, actual
map/account hit testing at deliberate overlap, held reply while log scrolled
or Sources focused, same-context hash query refresh preserving identity.
No removals or new files; at most two unit methods/four browser helpers.
Completed: exactly two unit methods and four helpers, zero removed assertions.
Actual route refresh calls show(), which focuses the workspace and dismisses
nonmodal chat without disposal. Assertions preserve this behavior and require
retained widget/draft/icon/toggle, consistent ARIA, then working open and close.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Document behavior

Update existing shared-chat README section for stacking, conditional following
and query-refresh toggle preservation, without tracking links in runtime docs.
Completed in the existing shared-chat section.

<!-- rpi:phase id=P02 -->
## P02: Validate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Commands

From src/api, export
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Use /tmp/mv/bin/{python,ruff,mypy}. Run chat-widget focus, chat panel/isolation/
fixture roles, resident chat/agenda/assistant units and case journey.
Enable ZF_BROWSER_TESTS for test_chat_panel. Run Ruff check ., format --check .,
isolated browser helper lint/format (project excludes checks), configured mypy
and node --check on widget/employee/resident adapter.
Run checks.chat_widget_browser_check with SHA-verified existing axe 4.10.3 and
new external output directory. Harness owns responsive loopback servers and
cleanup. No installs absent missing-dependency failure. No full discovery or
publication gate required by this bounded local-only candidate.
Executed: all static checks pass; 139 units pass, no skips; complete two-site
browser attempt5 passes. Original-code negative controls fail as expected.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Evidence

Record command exit status, assertion descriptions/results for findings 1-4,
tests/counts, logs/output paths, initial failures and corrections in changes.
Keep existing human/assistive-tech/live and hosted approval boundaries explicit.
Completed: command/result and four-finding matrix plus preserved adverse
attempts are in the changes artifact; no live/full-publication claim.

<!-- rpi:phase id=P03 -->
## P03: Review and persist

<!-- rpi:task id=P03-T01 -->
### P03-T01: One Review

Refresh guidelines, reconcile plan/details/changes and run one independent
Review against source, assertions and external validation evidence. Preserve
the original verdict; route findings to later work, never repeat Review.
Completed once: independent widget-fixes-independent-review, execution
Complete / outcome Conformant, no source defects. RV-001 is the distinct
future publication/acceptance obligation. Reviewer independently ran four
focus tests, three syntax checks and budget/diff checks; assessed other logs.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Local persistence

Resolve gh api user, configure repository-local privacy-safe email, commit
only scoped changes plus this dated evidence with required trailer. Verify
commit and worktree. No push or rubric edits. Complete local publication gate
is a future prerequisite, not claimed executed here.
The commit containing this closeout is the local persistence receipt; verify
its identity/trailer, clean worktree and unchanged rubric afterward. No push.
