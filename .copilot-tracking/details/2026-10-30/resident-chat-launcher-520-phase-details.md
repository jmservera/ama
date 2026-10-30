---
title: Resident chat launcher 520 phase details
ms.date: 2026-10-30
---

## Metadata

Task ID: 520. Task slug: resident-chat-launcher-520.
Plan: .copilot-tracking/plans/2026-10-30/resident-chat-launcher-520-plan.md.
Research: .copilot-tracking/research/2026-10-30/resident-chat-launcher-520-research.md.

## Phase Index

| Phase | Name | Status |
| --- | --- | --- |
| P01 | Preserve and expose grounded document answers | Complete |
| P02 | Validate and reconcile implementation evidence | Complete |

<!-- rpi:phase id=P01 -->
## P01: Preserve and expose grounded document answers

C1-C4 show data and safe fixed-topic rendering already exist, but ordinary
document wording is refused and typed AI prose can replace required facts.
Do not change source data, permissions, model configuration or agenda logic.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Extend bounded wording and fact-preserving dispatch

Targets: src/api/src/zava_forward/api/resident_demo/chat.py and app.py;
src/api/src/zava_forward/api/resident_demo/web/assistant.js.
Add finite complete document-question alternatives for missing/provision and
warning/error meanings. Keep safety, refusal, legal and consent precedence and
do not accept trailing unrelated requests. Reuse existing topic dispatch for
typed documents rather than duplicate advisor logic. Ensure disabled AI label
still explicitly says not enabled. Add a short question example in existing
intro; no markup/framework/style changes needed.

Completion: ordinary questions reach Topic.DOCUMENTS; all mandatory facts and
sources survive optional bounded selection, off/failure; other topics unchanged.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Reconcile regressions, browser cases and API guide

Targets: src/api/tests/test_resident_chat_api.py,
src/api/checks/resident_assistant_browser_check.py and src/api/README.md.
Keep existing test ownership. Removals: none. Maximum new test methods: 2.
Extend RECORD_QUESTIONS and own-record question cases; move the now-supported
warning question from the obsolete-refusal assertion. Remove documents from the
test asserting unconstrained typed prose, replacing with mandatory-fact coverage.
Use fake selector success plus failures/malformed output. Prove payload isolation,
no arbitrary model text, no loss of no-approval/no-upload boundary, protected
refusals and late revocation. Browser should ask supported normal questions and
assert the newest reply, facts and sources; existing agenda/focus/axe stays.
Update current README restrictions and document-generation description, preserving
historical dated evidence. No generated targets or new test files.

<!-- rpi:phase id=P02 -->
## P02: Validate and reconcile implementation evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run local gates and reconcile all plan markers

From src/api, use
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
with python3 -m unittest discover -s tests -q, ruff check ., ruff format --check .
and mypy; focused unit selectors precede discovery. Run node --check on changed
JS. Run actual checks.resident_assistant_browser_check with pinned axe,
external fresh output and no external application requests. Use
flock -w 600 /tmp/ama-rpi-heavy.lock for heavy gates.
Tool environment is external and task-owned if installs are needed.
Report exact counts/skips/failures, browser/axe evidence and pending human/AT.
Reconcile plan/details/changes and state before one independent Review.
No live model or live sign-in. Complete final gate follows the local commit;
missing prerequisites block publication, not excuse omissions.

Completion evidence: all planned edits integrated; 61 focused tests pass.
Task-owned pip environment imports this worktree. Full API discovery: 1380
tests in 481.873s, OK with 320 existing opt-in/integration skips. Ruff check
passes, 61 files formatted, mypy passes 117 source files. Changed JS syntax and
git diff checks pass. Actual local Chromium 156.0.8078.4 browser flow passes;
axe 4.10.3: 32 scoped scans, zero violations, incomplete checks retained (18
color-contrast, 25 aria-valid-attr-value entries). Human/AT acceptance pending.
