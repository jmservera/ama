<!-- markdownlint-disable-file -->
# RPI Plan: Workbook fuzzy-union correction

## Task Metadata

* Task ID: issue-146-pr-512-fix-cycle-1
* Task slug: monitoring-146-pr512-fix-cycle-1
* Date: 2026-10-29
* Planning status: Ready; single critique Complete / Revise, PC-001 rejected with rationale below.
* Details: .copilot-tracking/details/2026-10-29/monitoring-146-pr512-fix-cycle-1-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/monitoring-146-pr512-fix-cycle-1-plan-critique.md

## Executive Summary

Move each telemetry table's projection after its fuzzy union with the typed empty fallback. Add a focused workbook source-shape test that demonstrably fails on both old operands. Preserve all downstream monitoring semantics and validate locally, then perform one independent Review and commit without pushing.

### What You May Not Know

There is no tracked workbook-shape test to update. A new unittest in infra/tests will cover both query panels without unrelated test refactoring. Local source checks are not live Kusto execution or issue acceptance.

### Unresolved Decisions or Blockers

None for this bounded local fix. Publication and operational gates remain outside scope.

## User Decisions and Requirements

* Run full dated RPI for Refs #146 / PR #512 fix cycle 1; never use a closing keyword.
* First git pull --rebase (completed), reuse current branch, commit locally with the exact Copilot trailer; no push.
* Use bare AppRequests and AppAvailabilityResults union sources with project after union and retain typed empty datatables.
* Add/update query-shape regression that rejects the old form; validate existing infra/monitoring tests, JSON and Ruff check/format for Python changes.
* No Azure operations and no hand editing latest.json.

## Goals

* Correct absent-table fallback source binding without changing present-table sample calculations.
* Prevent regression of either query's union boundary.

## Scope and Non-Goals

In scope: Two initial KQL samples statements, one new infra unittest, a concise directly related infra README explanation, and this task's dated RPI artifacts.
Non-goals: Deployments, Azure queries/reads, latest.json changes, existing test cleanup, additional signals, issue closure, remote writes.

## Functional Requirements

* Each samples binding unions its original typed empty datatable with the corresponding bare table and projects the original fields after the union.
* Preserve the complete query suffix after the first semicolon, including sampling weights, filters, invalid-row counting, Insufficient status and null metrics.

## Non-Functional Requirements

* Workbook remains valid JSON; no dependencies added.
* Python test follows unittest and isolated repository Ruff policy.
* No cloud operations; any Bicep compilation in existing tests is local only.

## Acceptance Criteria

* Both old query prefixes fail the new test before the source correction; both corrected prefixes pass.
* Assertions cover typed fallback schema, bare source and post-union projection, not just fuzzy/datatable keyword presence.
* Existing focused infra/monitoring test group passes with no skips, along with JSON and changed-file Ruff checks.
* Independent critique and Review execution/outcome are recorded separately and preserved.
* Final local commit has Refs #146 and the exact Co-authored-by trailer; clean task worktree and no push.

## Sources

* .copilot-tracking/research/2026-10-29/monitoring-146-pr512-fix-cycle-1-research.md: C1-C4, Research executed / Ready.
* infra/monitoring-workbook.json: Canonical query source.
* infra/README.md: Monitoring limits and offline test commands.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and validate the source contract

Dependencies: Research Ready and single critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add regression, prove red, correct both queries and document

Add exactly one new test module, with one table-driven/subTest query-shape test covering requests and availability. Assert exact initial statement using the typed schemas and field order; run it before changing the workbook and record both failures. Replace only initial samples bindings, then prove green and unchanged downstream suffixes. Add a brief source-only contract explanation in infra README.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Run scoped validation

Run `PYTHONPATH=infra/tests REQUIRE_AZ_BICEP=1 python3 -m unittest test_monitoring_workbook test_bicep_policy test_iothub_module test_container_contract test_governance test_secret_lifecycle -q`; JSON parsing; isolated Ruff E,F,I,B,UP/py312/100 and format check for the new Python file; git diff --check. Use available /tmp/mv tools if needed without altering their environment or installed packages.

<!-- rpi:phase id=P02 -->
### [ ] P02: Independently review and commit locally

Dependencies: P01 complete and evidence reconciled.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute one independent Review

Reviewer activates rpi-review, compares task diff to starting head 5fc4ccc44a5ea15595560ea53e9941c1dd178fe6, reads validation evidence and records findings once. No new source fixes or repeated Review inside this completed cycle; route any findings to later work.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Persist outcome and make local commit

Use gh-resolved privacy-safe author/committer identity; stage only task paths; commit with Refs #146, no closing keyword and required trailer. Verify commit metadata, clean status and exact task paths. No full publication gate is needed for an expressly unpublished local commit; it remains mandatory before any later publication.

## Locked Change and Coverage Contract

* Test ownership: infra/tests/test_monitoring_workbook.py; maximum one new Python module and one test method covering both panels.
* Removals: none.
* Canonical targets: workbook, new test, infra README; generated targets: none.
* Semantic evidence: suffix equality and unchanged fallback types/field order.
* Regression evidence: red old source for both subtests, green fixed source.
* Validation evidence: requested scoped infra group, JSON parse, Ruff lint/format and diff hygiene; no Kusto/portal execution inferred.

## Dependencies

Python, existing local Bicep tool for offline policy tests and Ruff. Missing required validation prerequisites block success; no skip or cloud substitute.

## Critique Disposition

Execution: Complete. Original verdict: Revise. Exactly one critique performed; original artifact preserved.

| Finding | Owner | Disposition | Resolving evidence |
| --- | --- | --- | --- |
| PC-001 | Planning parent | Rejected: unsupported execution restriction | Parent runtime/repository/caller instructions contain no ban on /tmp tools or absolute external session paths; session files are explicitly supported and retention policy prefers external scratch. /tmp/mv/bin/ruff 0.17.1 was verified available without installation. Worker-only restrictions do not govern parent execution. Existing TemporaryDirectory tests remain unchanged. |

No unresolved significant/divergent finding or user decision. Readiness remains Ready with the original requested validation recipe. No repeat critique.

## Follow-Up Items

* None newly discovered. Historical operational/privacy/runtime/cost findings remain open and are not changed by this correction.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-29/monitoring-146-pr512-fix-cycle-1-changes.md.
P01 and P02-T01 complete: 92 scoped tests passed with zero skips, JSON valid, changed-file Ruff lint/format and diff hygiene passed. Red-before-green and unchanged query suffixes verified. Single independent Review Complete / Conformant, zero findings, precommit boundary only. Parent continues to P02-T02 local commit. No implementation blocker or user approval needed for the requested bounded local work.
