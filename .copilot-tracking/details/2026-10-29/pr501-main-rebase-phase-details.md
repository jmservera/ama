---
title: PR 501 main rebase phase details
description: Bounded conflict resolution and validation contracts
ms.date: 2026-10-29
---

Task ID and slug: `pr501-main-rebase`. Parent plan:
`.copilot-tracking/plans/2026-10-29/pr501-main-rebase-plan.md`.

## P01

P01-T01: Initial tree was clean. Research/plan/state are new task-owned
untracked evidence and must survive the rebase. Run `git rebase origin/main`.
At each conflict inspect all stages; rebase ours is upstream, theirs is the
replayed branch. Retain all index/log entries, upstream app structural changes
and the branch draft-only wording. Stage only resolved paths; continue with a
noninteractive editor. Do not stash or discard unrelated work.

P01-T02: Take `.github/rubric/` and
`docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`
from origin/main, regardless of score replay outcome. Confirm byte equality,
upstream ancestry, preserved branch copy and upstream refactor. Historical
evidence stays unchanged. No generator rewrite or manual source-hash change.

## P02

P02-T01: Use `/tmp/mv/bin/ruff check .`, `ruff format --check .`, and `mypy`
from both `src/core` and `src/api`. Core PYTHONPATH starts `src:tests`;
API adds `../core/src:../core/tests:../agents/src:../agents/tests` to
`src:tests` so imports cannot pick up another shared editable worktree.
Select `test_scenario_manifest`, `test_dependency_rule`,
`test_resident_decisions` in core and `test_content_standard`,
`test_design_system`, `test_accessibility_baseline`, `test_resident_api`,
`test_assistants`, `test_ui_support`, `test_dependency_rule` in API.
Inspect upstream added case/chat tests after rebase and include directly
relevant modules. Run `node --check` on the four edited JS assets.
Existing synthetic browser checks may run only locally; no paid/cloud path.
Do not run full API discovery. Do not mutate shared venv unless a chosen
command actually proves a missing dependency and its manifest already owns it.
Current-state adaptation: preserve main's edited-proposal submit label in
the content test, and select the Resident tab explicitly in the existing
resident browser login helper. No test methods removed or added.

P02-T02: Changes artifact records each command, exit result, unit totals/skips,
actual conflict paths and resolutions. Verify `git diff --check`, no conflict
markers, source/test layout, upstream canonical files and append-only entries.
Failures require a tightly scoped fix and rerun before Review.

## P03

P03-T01: Fresh independent reviewer activates `rpi-review`, checks the exact
source delta against fetched main and plan completion; writes only the dated
Review artifact. Refresh web rules for changed web lines. No second Review.
No human or hosted approval is inferred. Route findings to later work.
PC-001 disposition: only a passing independent Review without unresolved
blocking findings permits successful candidate closeout. Record nonblocking
follow-up owners and rationale. A blocking Review stops the success claim;
do not repeat Review or imply a later source correction was independently
reviewed at the old boundary.

P03-T02: Authenticated GitHub account resolved to login jmservera, id 8036360.
Repository-local noreply email configured. Commit only task-owned changes
and RPI evidence using Conventional Commit, Refs #153 and Copilot trailer.
Never push, create/modify Azure resources or edit issue acceptance. Verify
clean tree, final base ancestry, local commit and unchanged remote branch.
Complete publication gate is deferred, not passed, because coordinator owns
publication and this task requests bounded local checks and no push.

## Pre-Review reconciliation

P01 and P02 complete. One rebase completed, all intended source deltas and
append-only preservation verified. Ruff/format/mypy core/API pass. Core
182 tests/64 skips and API 191 tests/51 skips pass; skips are preserved
opt-in integrations/nonapplicability, not fresh integration acceptance.
The opt-in resident browser was then explicitly enabled and passed with no
skip after adapting its route. Existing design/workbench and current case-view
browser checks pass in Chromium. Source hash and exact commands are recorded
in changes. No method removals/additions, dependency install, cloud action,
full API suite or push. P03 remains for independent Review and local commit.

## Final local completion

P03-T01 Complete / Conformant with justified divergence, no findings.
P03-T02 committed as `57ec5c95d17cf45c67aa894bec65dca0f402a42a`; author and
committer use the authenticated noreply identity, message Refs #153 with
required Copilot trailer. Post-commit tree was clean and main ancestry passed.
All P01-P03 tasks complete for local scope. Final evidence-only bookkeeping
does not change source or expand the independent Review's assessed boundary.
Coordinator publication/full receipt/hosted checks and human acceptance remain
separate work. No push or Azure action occurred.
