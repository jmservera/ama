---
title: Masked chat question length changes
description: Original implementation and validation evidence for issue 157
ms.date: 2026-10-29
---

# RPI Changes: chat-masked-length-157

## Metadata

* Task ID: 157-chat-masked-length-2026-10-29
* Related plan: .copilot-tracking/plans/2026-10-29/chat-masked-length-157-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/chat-masked-length-157-phase-details.md
* Implementation date: 2026-10-29
* Baseline: e833fc8c, feat/agent-chat-157, PR #503 / issue #157

## Execution Status

Implementation, focused validation and single independent Review complete.
Full plan scope. P01/P02 and all task markers complete; final delivery evidence
is persisted by the authorized local commit containing this record.
Approved write boundary: core chat_panel.py, owning tests, existing directly
related guide and this task's dated tracking artifacts.
Single critique Complete / Pass, no findings or additional user decisions.

## Execution Summary

Reject expanded redacted questions above 1,000 characters, preserving original
length checking, inclusive cap, refusal order and ordinary fallback persistence.
Captured regression red, implemented the guard and validated green.

## Completed Work

### P01-T01: Regression and inclusive boundary

Added exactly two StoredQuestionTests methods, no removals, seven modes each.
The corrected pre-fix run executed 2 tests, exit 1, seven overflow subtest
failures: actual abstain/ABSTAIN instead of fallback/LIMIT_REACHED. The exact
masked-cap test passed with full question dispatch. Production was unchanged
for this run. Original red outcome is retained here; no acceptance claimed.

### P01-T02: Masked admission guard

Extended the existing raw-length condition with strict masked-length overflow,
reusing the current LIMIT_REACHED finish path. Added a concise limit explanation
beside the employee panel history guide in src/core/README.md. No changes to
refusal order, redaction, storage/audit, cap, prompt escaping or dependencies.
Green validation: focused core and API chat tests pass; lint/format/type pass.

### P02-T02: Independent Review and local-only delivery

Independent Review execution Complete; outcome Conformant; no substantive
findings. Review artifact:
.copilot-tracking/reviews/logs/2026-10-29/chat-masked-length-157-review.md.
Independent evidence: 11 pure tests, 28 memory-only scenarios, changed-file
Ruff lint/format and diff checks passed. Raw-only overflow after redaction
contraction and refusal priority were independently checked.
Original Review remains unchanged; no in-task correction or repeat Review.

All original dated artifacts and the three scoped core files are included in
the containing local Conventional Commit. Parent immediately verifies commit
identity/trailer, paths and clean status. Author/committer identity is the
authenticated account's 8036360+jmservera@users.noreply.github.com, configured
repository-locally. No push, az or rubric edit is authorized or performed.

## Implementation-Time Plan and Detail Updates

Ordinary local fixture correction: existing response field is `reply`, not
`text`; corrected before valid regression red. No significant divergence,
amendments, dependency changes or changed owner decisions.
Plan task markers, phase-details status and handoff now reflect completed
implementation/validation/Review and atomic local delivery. No new source
changes follow Review. Commit helper's referenced instructions path was stale;
resolved and read the actual rules/hve-core/commit-message.instructions.md.
Its get_changed_files tool is not exposed here; staged-path inspection uses
the available Git CLI and explicit task-only staging under repository rules.

## Validation Record

Existing .venv: Python 3.12.3, Ruff 0.17.1, editable source matches this worktree.
Reproduction verified: 977 raw / 2,297 masked characters; trailing question
disappears in existing neutralise(..., 1000). Opposite boundary 989 raw / 1,000
masked. Test execution in progress. First overflow run exited 1 with seven KeyError
errors: the new test used `text` instead of the existing response key `reply`.
Corrected the test field without changing production; this is fixture correction,
not evidence of the production defect. The corrected unchanged-source red run
is preserved in the table below.

All commands below use the existing ../../.venv/bin/python from the named
project directory. No dependencies installed or upgraded.

| Check | Command / directory | Result |
| --- | --- | --- |
| Corrected pre-fix regression | core, PYTHONPATH=tests, -m unittest test_chat_panel.StoredQuestionTests.test_expanding_redaction_over_question_limit_falls_back_without_dispatch test_chat_panel.StoredQuestionTests.test_expanding_redaction_at_question_limit_dispatches_complete_question -q | Exit 1; 2 tests, seven expected overflow subtest failures; exact-cap test passed |
| Focused core chat | core, PYTHONPATH=tests, -m unittest test_chat_panel test_chatthreads test_chat_privacy test_chat_memory -q | Exit 0; 85 tests, no skips |
| Focused API chat | api, PYTHONPATH=tests:../core/tests:../agents/tests, -m unittest test_chat_panel test_chat_isolation -q | Exit 0; 70 tests, one existing opt-in local Chromium skip |
| Ruff lint | core, -m ruff check . | Exit 0; All checks passed |
| Ruff format | core, -m ruff format --check . | Exit 0; 108 files already formatted |
| Types | core, -m mypy | Exit 0; 161 files, no issues |
| Diff whitespace | root, git diff --check | Exit 0 |
| Rubric untouched | root, git diff --name-only -- .github/rubric/scores/latest.json | Empty |

API skipped test:
PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log,
decorated with ZF_BROWSER_TESTS opt-in. No web changes; browser acceptance
not claimed. The suite also emitted law-store-unloaded diagnostics from its
existing synthetic fixtures; no failures resulted.

## Pre-Review Reconciliation

Ready for independent Review of bounded implementation. Plan markers/details,
completed work, validation, handoff and remaining delivery task are reconciled.
P02-T02 is explicitly incomplete until Review and commit; no material source
blockers or deviations. Critique remains the original Complete / Pass.

Post-Review parent reconciliation: Review Complete / Conformant; all tasks
now have evidence, and this final delivery record is persisted atomically by
its containing local commit. The original pre-Review and Review outcomes above
are preserved. No findings require a later implementation phase.

## Blockers

None for bounded local fix. Complete publication gate and hosted/human/live
acceptance are not established or authorized. No az or push will run.

## Remaining Work

No source or RPI phase work remains. The containing local commit persists the
final delivery record; only immediate local commit/worktree verification
remains for the parent. Publication is excluded.

## Follow-Up Items

Existing publication/hosted/human/activation gates remain outside this task.
No new implementation follow-up selected.

## Return-to-Caller State

Full requested loop complete: manual mode, session stopped, phase Follow-up.
Review execution Complete, outcome Conformant, no findings or fix follow-ups.
Parent persists this record via local commit and verifies it, then stops.
Existing publication/hosted/human/activation gates remain unmet and require
separately authorized future work. No push or new child task.
