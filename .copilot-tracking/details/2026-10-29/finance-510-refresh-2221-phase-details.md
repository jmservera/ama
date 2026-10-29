<!-- markdownlint-disable-file -->
---
title: Finance 510 current-main refresh phase details
description: Task-level execution and completion expectations
ms.date: 2026-10-29
---

Task ID / slug: `finance-510-refresh-2221`. Plan:
`.copilot-tracking/plans/2026-10-29/finance-510-refresh-2221-plan.md`.
Research disposition executed / Ready, C1-C8. No local implementation blocker.

<!-- P01 -->
## P01: Integrate fetched main

<!-- P01-T01 -->
### P01-T01: Replay upstream

Initial clean finance HEAD `6a0a6d95`, remote bot `011f6a6e`, main `129808b3`.
Use `git merge --ff-only origin/docs/finance-96` to preserve the known upstream
commit, then `git rebase origin/main`. Verify main identity before replay.
Only current task's newly created evidence may be untracked at this boundary;
no pre-existing owner changes were present or are being moved.

<!-- P01-T02 -->
### P01-T02: Resolve and prove

Use conflict stages and main/topic diffs. Preserve main's full log as prefix
and append topic entries; index keeps both entries. Component READMEs keep
both finance and safety sections. Store composition retains both domain hooks.
Restore complete `.github/rubric` and scenario manifest from immutable main
where necessary. Original evidence must remain byte-identical.
Prove main ancestry, no unmerged entries and exact protected-file equality;
compare source against old topic and main to distinguish inherited changes.
Re-run manifest test and verify its four pinned source paths.

<!-- P02 -->
## P02: Validate and deliver locally

<!-- P02-T01 -->
### P02-T01: Existing static/regression checks

Core cwd `src/core`, API cwd `src/api`.
Core PYTHONPATH:
`src:tests:../api/src:../api/tests:../agents/src:../agents/tests`.
API PYTHONPATH:
`src:tests:../core/src:../core/tests:../agents/src:../agents/tests`.
Set `PYTHONDONTWRITEBYTECODE=1`; use no-cache Ruff and mypy cache `/dev/null`.
Set `TMPDIR="$PWD"` and assert `tempfile.gettempdir()` resolves to that cwd.
Assert imports point at fin96, not installed editable sibling.
Run each project's complete Ruff/check/format/mypy.
Core selectors: `test_form_review test_form_review_pack test_form_staging
test_finance_match_controls test_finance_signoffs test_grant_lifecycle_controls
test_change_provenance test_document_rescan test_scenario_manifest
test_dependency_rule test_resident_decisions`.
API selectors: `test_form_staging_api test_finance_match_api
test_role_endpoint_inventory test_dependency_rule test_resident_api`.
Full API discovery is optional additional evidence and must hold the heavy
lock for its entire run; never launch if nonblocking acquisition fails.
Record skip counts without claiming real SQL or browser coverage.

<!-- P02-T02 -->
### P02-T02: Single Review and local commit

Reconcile plan/details/changes and executed validation before Review.
Fresh independent reviewer writes only
`.copilot-tracking/reviews/logs/2026-10-29/finance-510-refresh-2221-review.md`.
Scope is current rebase/resolution plus this task's evidence, not re-approval
of all historical finance delivery. Route findings to later work, no repeat
Review. Any material integration/validation finding blocks ready/accepted
handoff; preserve original outcome and name unresolved work explicitly.
Confirm GitHub identity, set local noreply email, stage exact changes
and commit a Conventional message with references and Copilot trailer.
No push. Preserve full-gate/publication residual honestly. Changes and state
are persisted before/after lifecycle transitions.

## Completion State

P01 complete at replay HEAD `813d038d4e528a9fa1d91ba3f872d6412fea26fb`.
P02-T01 complete: static/focused checks and held-lock full API discovery pass.
Core 431 tests/130 skips; API focused 44/1; full API 1344/318.
Migration guard rerun in dependency-complete `/tmp/mv` passes 25 tests after
the system interpreter's missing optional pptx/PIL imports.
P02-T02 single Review and local commit remain pending.
Single Review now Complete / Residual work on original replay/base. During
local commit preparation main advanced to `719e76e5`; parent closeout replays
that explicit current-main direction and revalidates without another Review.
Final exact-head publication assessment remains coordinator-owned.
Refreshed replay `561ac4c5` on main `719e76e5`: all nine patches equal prior
assessed series; no Python/test/config change. Final core/API static checks
and 258/44 focused tests pass. Final local evidence commit remains pending.
No tests/source added or removed. Original critique and Review outcomes from
other tasks remain immutable.
