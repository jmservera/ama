<!-- markdownlint-disable-file -->
# RPI Phase Details: issue-172-chat-fixture-isolation

## Metadata

Task ID: 172. Date: 2026-10-18. Task slug: issue-172-chat-fixture-isolation.
Plan: .copilot-tracking/plans/2026-10-18/issue-172-chat-fixture-isolation-plan.md
Research: .copilot-tracking/research/2026-10-18/issue-172-chat-fixture-isolation-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Strengthen fixture contracts | Complete; failing-first then 15 tests OK | P01-T01, P01-T02 |
| P02 | Document and validate | Complete; focused/public 54, agents 98 tests and quality gates OK | P02-T01 |
| P03 | Original Review/publication gate | Pending | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Strengthen fixture contracts

Context: baseline 11 tests pass; memory masks resource-specific owner coverage.
Intent: add meaningful contractor actor coverage without changing task eligibility.
Boundary: helper/test only; no runtime. Completion: focused green tests with
recorded failing-first regression. No engineering blocker.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Establish resource-specific and contractor coverage tests

Use persona eligible_tasks to independently derive expected thread owners.
Assert thread-owner equality and same-role thread probe owner equality, exact
per-owner read/list/search matrix, roles, resource ownership and denied outcomes.
Retain eleven-perspective assertion for existing memory/combined probes only.
Both contractors must have empty tasks and zero owned threads. Shared test
assertion verifies contractor kind/action/owner/resource/active target and matrix;
exercise it against real output and modified copies missing each denial action,
self actor/owner, or invalid/mismatched resource target. Prove omissions fail.
No existing tests removed; at most six added methods.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Generate explicit contractor denials

After tests expose gap, add `contractor_access_denied` kind in existing
`isolation_cases()`. Select first active thread whose owner has that task in
eligible_tasks and is not Contractor. Reuse that real target for both contractors
and read/list/search. Deterministic list traversal; no RNG or schema overhaul.
If contractors are present but no valid target exists, raise ValueError with
clear diagnostic; add direct no-target test. Do not self-pair or fabricate target.
Existing output generators, lifecycle and nine payload names remain intact.

<!-- rpi:phase id=P02 -->
## P02: Document and validate bounded evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update evidence and run checks

Targets: dictionary chat fixture section, agents README, KB index and append-only
log. Explain all eleven persona perspectives, current seven eligible thread
perspectives, six explicit contractor denials, and no runtime enforcement claim.
No needs-inventory status change; scope/volume remains open.

Commands: root focused unittest modules using `.venv/bin/python` and absolute
test-helper PYTHONPATH; agents component discovery with core-test helper path;
from src/agents use local venv Ruff check ., Ruff format --check ., mypy.
Run `test_synthetic_provenance`, `test_scenario_manifest`, `test_needs_inventory`
and agents `test_eval_registry` as relevant public coupling checks. Existing
scenario source hashes exclude chat helper, so no refresh needed. Existing
`chat_fixture.write()` and privacy checker validate freshly computed aggregate
hashes for all nine payloads; no output gets committed. Rename regression is
only relevant if migration paths/metadata change; otherwise mark not applicable.
No SQL/Azure/AI/browser or deployment acceptance applies; do not imply those ran.
Record all actual results and baseline dependency recovery, with current
migration lint/format/type exclusions disclosed.

Execution: focused fixture/provenance/roles passed 15; combined public coupling
passed 54; agents discovery passed 98. Existing Ruff check/format and mypy passed.
No migration path or metadata changed, so rename regression is not applicable.
Helper/test keep existing migration format exclusion and mypy ignore_errors;
green exits are not newly strict formatting/type coverage for these files.
Dictionary/README/index/log updated, SN-08 untouched. No source digest or frozen
snapshot refresh was required. No implementation amendment or divergence.

<!-- rpi:phase id=P03 -->
## P03: Original independent Review and publication gate

<!-- rpi:task id=P03-T01 -->
### P03-T01: Execute exactly one original Review

Independent worker gets plan/details/critique/research/changes/state and complete
diff, uses rpi-review once, writes one original artifact only, no source edits.
Review checks bounded semantics, tests/mutations, preservation, provenance,
privacy and claims. Acceptance is bounded engineering, not #172 closure.
Adverse Review is immutable and blocks push/PR; parent commits local frozen
evidence and routes coordinator maximum-two corrections, never re-reviews.
Accepted work is committed with fresh gh identity and privacy-safe local email,
Conventional Commit and Copilot trailer, normal pushed and main PR opened.
No merge, rebase, force push, AC/issue/board edits, or paid rubric dispatch.
