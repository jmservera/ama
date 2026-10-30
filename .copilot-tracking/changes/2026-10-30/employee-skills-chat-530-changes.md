<!-- markdownlint-disable-file -->
# RPI Changes: employee-skills-chat-530

## Metadata

* Task ID: 530; date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/employee-skills-chat-530-plan.md.
* Details: .copilot-tracking/details/2026-10-30/employee-skills-chat-530-phase-details.md.

## Execution Status

Partial; full plan scope. P01/P01-T01 and P02-T02 complete. P02-T01 blocked on
heavy-lock admission. P03 independent Review/local handoff remains. No runtime
or web source file changed.

## Execution Summary

Existing delivery retained. Add exactly two shared regressions in the existing
test owner, then validate locally. PC-001 ownership/secret handling applied
directly; the original Complete / Revise critique remains intact.

## Completed Work

### Shared skill storage acceptance (P01-T01)

src/core/tests/test_chatthreads.py adds exactly two ChatBehaviour methods and
needed imports. JSON/SQLite each exercise six cited one-call skill selections,
masked stored question, citations, skill/outcome/question-sequence audit after
reopen, unchanged case and valid audit chain; general mode lacks case facts,
foreign owners cannot infer/store, missing and timed-out models fall back.
Every new SQL store instance registers its connection cleanup. Existing actual
MssqlChatThreads inherits both methods without adding another harness.

### Current documentation (P02-T02)

src/api/README.md records the dated local refresh and incomplete heavy/live
evidence. Historical Review RV-003 and all earlier artifacts remain unchanged.

## Implementation-Time Plan and Detail Updates

PC-001 applied directly before implementation. No material source divergence.
External one-off batch script was prepared in the session files, but never
executed because lock admission failed. It cannot count as SQL safety/run proof.
Heavy-gate failure is a validation blocker, not evidence of a source defect.
No retry, cloud fallback, foreign-resource use or full receipt claim.

## Validation Record

External evidence root: /tmp/ama-530-local-20261030-M3hRQX.
Interpreter: Python 3.12.3, /tmp/mv/bin/python; installed src distributions,
Ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0. All executed tests set
PYTHONDONTWRITEBYTECODE=1 and explicit current-worktree source/test paths.
No uv/install/cloud/model/sign-in/credential-file access occurred.

| Check | Status | Evidence |
| --- | --- | --- |
| Four exact new MemoryChatTests/SqlChatTests methods | Pass, 4 tests, 1.840s, no skips | focused-new-tests.log |
| Eight targeted HTTP PanelTests | Pass, 8 tests, 3.387s, no skips | api-targeted.log |
| API Ruff check . | Pass, exit 0 | api-ruff.log |
| API Ruff format --check . | Pass, exit 0 | api-format.log |
| API mypy | Pass, 116 files | api-mypy.log |
| Core Ruff check . | Pass, exit 0 | core-ruff.log |
| Core Ruff format --check . | Pass, exit 0 | core-format.log |
| Core mypy | Pass, 165 files | core-mypy.log |
| Consolidated flock -w 600 /tmp/ama-rpi-heavy.lock batch | Blocked, exit 1 before execution | shell 530-local-gates, no output |
| Requested complete API unittest discovery | Not run, heavy lock unavailable | No pass inferred from targeted tests |
| Fresh employee Playwright/axe | Not run, heavy lock unavailable | Earlier browser evidence is historical |
| Actual SQL MssqlChatThreads | Not run, heavy lock unavailable | No container created |
| Complete publication gate | Not run, invokes prohibited Azure CLI | No receipt |
| Live site/model, human acceptance/name confirmation | Not performed, outside authorization | Whole AC8 remains unmet |

Focused HTTP selector names:
test_all_five_skills_and_general_use_one_bounded_model_turn,
test_general_help_has_workflow_sources_and_no_record,
test_skill_help_never_bypasses_role_projection_or_privacy_gate,
test_skill_scope_and_thread_owner_rechecked_without_inference,
test_model_failure_falls_back_to_workflow_only,
test_skill_question_outcome_audit_contains_reference_not_content,
test_invalid_skills_do_not_store_or_infer,
test_skill_source_change_during_call_withholds_and_keeps_usage.

The initial focused heavy-lock wait was cancelled before executing any test to
consolidate heavy work in one batch; its replacement timed out. A separate
explicit-file Ruff format diagnostic bypassed the existing excluded-file policy,
reported both inherited and new formatting and prevented that chained mypy
command. The later configured component format and mypy commands pass. No
format exemption was added or changed.

## Pre-Review Reconciliation

Plan/details/changes agree: P01 and P02-T02 complete; P02-T01 remains incomplete.
Ready for independent Review of the bounded test/doc diff with validation gaps
explicit, not a conformant/publication-ready claim. No web files changed.

## Blockers

Heavy lock unavailable for the full authorized 600-second wait; full API,
browser/axe and actual SQL remain blocked until a later coordinator-admitted run.
Complete publication gate invokes prohibited Azure CLI; live verification/name
confirmation requires separate owner authority. No full receipt exists.

## Remaining Work

P02-T01 heavy checks and P03 local commit. The single independent Review is
Complete / Not accepted, RV-001 High: required current local evidence missing.
No new source defect found. Reviewer could inspect the diff and canonical
records, but could not open the external /tmp logs under its own access
restriction; focused/static passes remain parent-executed observations, not
independently authenticated raw logs.

## Follow-Up Items

Owner/coordinator: full publication gate, live acceptance and name confirmation.

## Return-to-Caller State

The single Review is complete with outcome Not accepted. Parent will commit
the bounded test/documentation candidate and original dated RPI records locally,
then route RV-001 to later evidence collection. No second Review or remote write.
