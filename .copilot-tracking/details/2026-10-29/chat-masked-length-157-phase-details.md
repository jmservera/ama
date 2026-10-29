---
title: Masked chat question length phase details
description: Evidence and task-level completion criteria for issue 157
ms.date: 2026-10-29
---

# RPI Phase Details: chat-masked-length-157

## Metadata

* Task ID: 157-chat-masked-length-2026-10-29
* Task slug: chat-masked-length-157
* Plan: .copilot-tracking/plans/2026-10-29/chat-masked-length-157-plan.md
* Research: .copilot-tracking/research/2026-10-29/chat-masked-length-157-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Correct question admission | Complete | P01-T01, P01-T02 |
| P02 | Validate and preserve evidence | Complete; final record persisted by containing local commit | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct question admission

Research C1-C5 establishes the raw-only guard and truncating neutralise call.
Do not alter refusal ordering, storage/audit, cap, redaction or scope.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add regression and inclusive-boundary coverage

Use StoredQuestionTests (synthetic Store, current permitted user, prompt spy).
Create a thread for the first permitted synthetic case for each of None,
"general" and the five REGISTRY keys so the legacy path has real sources.
Add at most two methods, no removals or generated outputs.

Overflow fixture: "NE1 1AA " * 120 + "What stage is it?".
Assert raw below cap, masked above cap and actual lengths 977/2,297. Call
panel.ask directly; do not use the helper that assumes model dispatch.
Assert LIMIT_REACHED, fallback, workflow_only, empty citations, workflow-only
model and consumption.model_calls == 0; prompts must stay empty. Preserve
stored masked question and fallback reply.

Boundary fixture: "x" * 981 + " NE1 1AA", raw 989 / masked 1,000.
Check the full masked text is present at the end of the actual dispatched
Question field and model_calls == 1. This test is semantic coverage of the
inclusive cap, not merely a repeated overflow test.

Run the overflow selector against unchanged source to capture expected failure.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Extend the existing length guard

Change only the admission condition to raw-too-long OR masked-too-long.
Both are strict greater-than MAX_QUESTION_CHARS. Continue through existing
finish path so receipt/provider_outcome and persisted turns retain behavior.
No separate raw text, helper, cap or privacy logic is needed.
Review existing project chat/limit documentation and clarify locally if present.
Completion: new regression and opposite boundary both pass.

<!-- rpi:phase id=P02 -->
## P02: Validate and preserve evidence

P01 is prerequisite. The full local publication gate is not run because no
publication is authorized and the owner forbids az. Never replace it with a
claim that focused checks constitute full acceptance.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused validation and reconcile evidence

From src/core with ../../.venv/bin/python and PYTHONPATH=tests:
`-m unittest test_chat_panel test_chatthreads test_chat_privacy test_chat_memory -q`.
From src/api with PYTHONPATH=tests:../core/tests:../agents/tests:
`-m unittest test_chat_panel test_chat_isolation -q`.
From src/core: `../../.venv/bin/python -m ruff check .` and
`../../.venv/bin/python -m ruff format --check .`.
Only restore/install existing dependencies after an actual missing-dependency
failure. Capture exits/counts/skips. Review diff and ensure rubric is unchanged.
Reconcile plan checkboxes, details and changes before Review.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Independent Review and local commit

Fresh independent worker activates rpi-review, reads exact plan/research/changes
and scoped diff, writes only
.copilot-tracking/reviews/logs/2026-10-29/chat-masked-length-157-review.md.
Single Review execution; route findings to later work, do not loop in-task.
Preserve original findings and keep required human/hosted acceptance unclaimed.

Commit source, tests, any directly related guide and dated evidence only.
Authenticated GitHub identity id 8036360/login jmservera gives repository-local
email 8036360+jmservera@users.noreply.github.com for author and committer.
Use Conventional Commit plus
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>.
Verify local commit and clean worktree; no push, az or rubric score edits.

## Unresolved Items

None for bounded implementation. Full publication and operational approvals
remain separate, unmet and unauthorized.

## Completion Evidence and Review Handoff

P01-T01: two methods added; pre-fix red run had seven expected overflow
subtest failures, while exact-cap acceptance passed. P01-T02: single guard
extension and core guide paragraph; all new tests green.

P02-T01: focused core suite 85 passed/no skips; API suite 70 run/one existing
opt-in Chromium skip. Core Ruff check and format --check passed (108 files);
core mypy passed (161 files). git diff --check passed; rubric file unchanged.
API fixtures emitted existing law-store-unloaded diagnostic logs but exited 0.
No browser, actual provider, complete local gate or hosted/human acceptance
is claimed. No source changes outside the approved boundary.

P02-T02: single independent Review Complete / Conformant, no findings.
Original Review record is unchanged. This final evidence is persisted by its
containing authorized local commit; parent verifies local commit identity,
trailer and clean worktree immediately afterward. No further source changes
or Review execution; no publication acceptance or push.
