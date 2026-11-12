<!-- markdownlint-disable-file -->
# Review: Legacy AI usage attribution (Refs #432, initial slice)

## Scope and Evidence

* Task ID: legacy-ai-usage-attribution-432-1112; base 139176fa0382add781b1830b1ac9db785ed086fe; branch feat/demo-legacy-ai-usage-432-1112.
* Plan: .copilot-tracking/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan.md
* Details: .copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-12/legacy-ai-usage-attribution-432-1112-changes.md
* Research: .copilot-tracking/research/2026-11-12/legacy-ai-usage-attribution-432-1112-research.md
* Boundary reviewed: git diff of src/core/src/zava_forward/core/ai.py, src/api/tests/test_ai_consumption_api.py, docs/reference/resources/ai-tokenomics.md, docs/reference/log.md against the base. This is the task author's own original Review; it is not the required independent exact-head review.

## Opening Review State

Implementation finished; plan markers checked; changes record current; one Review run, no subagent lens used (single small diff read directly).

## Execution Status

Complete.

## Plan-to-Change Reconciliation

| Item | Evidence | Result |
| --- | --- | --- |
| P01-T01 tests | five methods in test_ai_consumption_api.py, case table in details | Matches; fewer than the six-method cap |
| P01-T02 reorder | ai.py diff: two statements swapped, one comment | Matches, nothing else changed in source |
| P02-T01 docs | tokenomics sentence and log entry | Matches |
| P02-T02 validation | changes Validation Record | Recorded with counts |

## Completed Work Assessment

* Failing-first is evidenced: the settlement-failure test failed on unfixed source and passes after the fix.
* The test handler change keeps the default usage payload identical, so existing tests are unaffected (129, 52 and 13 targeted tests pass).
* The tests assert no raw prompt or provider text in ledger records; no network or model call; only the loopback spy.

## Implementation-Time Plan and Detail Update Assessment

Two descriptive updates in the changes record (malformed-usage assertion matches observed unchanged behavior; five methods instead of six). Neither changes scope, requirements or evidence boundary; both are justified.

## Critique and Material Revision Assessment

One critique, Revise, five direct planner-applied findings, no user decision and no second critique. All dispositions are reflected in the plan and details.

## Plan Follow-Up Assessment

Plan follow-ups (look_at and priority proof; resident chat host join) remain outside this task and are routed below.

## Findings

### RV-001 [Low]: Malformed usage still shows AI draft text with an Unknown ledger liability

* Evidence: new test `test_legacy_draft_missing_or_malformed_usage_is_unknown` asserts the output is joined and the ledger is held with Unknown, yet `ai_tasks.finish` only routes to the manual route on a `publish_output` hold.
* Impact: cost attribution is Unknown (correct), but whether an unknown-liability draft should be withheld is an unmade product decision; behavior is unchanged from main.
* Destination: rpi-plan (decision gap, not a defect of this change).

### RV-002 [Low]: Issue body still says legacy paths discard usage

* Evidence: issue #432 summary; this task did not edit issues by direction.
* Destination: distinct follow-up for the owner or a later authorised action.

### RV-003 [Low]: Process deviation

* Evidence: the test edits were applied with a one-off Python script instead of the edit tool, contrary to the repository's file-change rule. The resulting diff was reviewed here and the formatter and tests pass; the content is unaffected.
* Destination: residual note only.

## Defects

None found in the reviewed boundary.

## Routed Findings

| Finding | Destination |
| --- | --- |
| RV-001 | rpi-plan, owner decision |
| RV-002 | distinct follow-up, owner |
| RV-003 | note |

## Residual Work

* `look_at` and priority envelope-usage proof; resident chat host join (owner-gated, authority window ended 2026-11-01); the zero-prompt-token difference with the assistants path (unevidenced).

## Blockers and Remaining Work

None. Not performed: full gate, SQL Server, browser, hosted CI, independent exact-head review, human approvals.

## Validation Evidence

Baseline 32 tests; new 5 tests (1 failing-first); after fix 129 api, 52 core, 13 agents targeted tests OK; ruff check and format and mypy pass on the test file; ai.py `ruff format --check` fails on pre-existing style and was not altered. Evidence class: local observed on constructed synthetic data; no cost, price, billing or authority claim; no criterion tick.

## Outcome

Residual work. Defects: none. Findings: 0 Critical, 0 High, 0 Medium, 3 Low. This Review is the author's own; independent exact-head review and applicable hosted CI remain required before publication.

## Closeout Routing Record

Review executed once; no return to Implement or Review inside this task.
