---
title: Issue 108 evaluation run accounting phase details
description: Executable task boundaries and completion evidence
ms.date: 2026-10-18
---

## Metadata

Task ID 108; slug issue-108-evaluation-runs; date 2026-10-18.
Plan: .copilot-tracking/plans/2026-10-18/issue-108-evaluation-runs-plan.md.
Research: .copilot-tracking/research/2026-10-18/issue-108-evaluation-runs-research.md.
Current status: P01-P03 complete; PR #405 published, coordinator exact-head review next.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Behavioral regression and red baseline | Complete |
| P02 | Minimal accounting/contract repair | Complete |
| P03 | Local validation, one Review, publication | Complete |

<!-- rpi:phase id=P01 -->
## P01: Lock regression evidence

Context C1/C2/C5: transient recs already exist; summary discards identities.
No production edits until the new focused tests reproduce the missing contract.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Focused regressions

Use tempfile stores and existing golden scenarios; no new fixture file.
Load constructed golden cases and copy before mutation. Capture returned Store
recommendations with a wrapper, change only returned metadata for varying
model/prompt/null identity tests, and compare report rows to captured results.
Use valid/invalid model output in both orders and repeated no-model cases.
Check reviewer ID and reviewed recommendation ID stay on the final result,
and summary counts do not multiply by runs. Assert legacy quality values
against the final result, not a newly averaged metric.
Negative control disables store critical guard, supplies an early safety miss
then a valid result and requires harness failure. Existing citation/authority
negative controls remain. At most seven new test methods; none removed.
Completion: red unittest log showing missing/new accounting contract at base.
Actual evidence: issue-108-evaluation-runs-red.log, 13 methods run with two
failures and six errors (both mixed-order subtests included); baseline production
source unchanged. Project-local TMPDIR resolution verified.

<!-- rpi:phase id=P02 -->
## P02: Evidence-faithful report repair

Depends on P01; no core runtime changes expected.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Report implementation

Targets: src/agents/src/zava_forward/agents/ai_eval.py.
Construct ordered `run_results` from the already returned recs and measured
latencies, before the extra workflow comparator. Retain exact returned identity,
source and model-latency values, not hardcoded scripted model names. Add reviewer
and final recommendation binding to the existing single review record.
Summary flattens this canonical run evidence for source counts and identity sets;
it keeps scenario summaries for quality and one reviewer action. Keep final-only
quality assumptions explicit; models retained on fallback are not reclassified.
Scope excludes provider attempts, tokens/cost, serving attestation and new gates.
Completion: focused green tests and unchanged existing golden quality/failure
values. A transparent source-label validity check may fail invalid source
metadata rather than silently accepting an unaccounted category.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Direct consumers and README

Targets: src/agents/README.md and src/api/tests/test_ai_tasks.py.
Document corrected `ai_runs`, additive fields, overlapping source-scenario counts,
latency semantics, last-only legacy quality and exclusion of text-task/comparator
runs. Labels do not attest actual model/version or provider calls.
Assert pass-through endpoint report reconciliation using its returned rows.
No browser, API server, registry, golden or KB change.
Completion: narrow diff and existing API negative controls/endpoint tests pass.

<!-- rpi:phase id=P03 -->
## P03: Validation, Review and bounded publication

Depends on P02; local evidence precedes remote publication.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Local validation

Use isolated pip-installed distributions after the recorded actual import failure.
Every application/test process uses `env -i` with explicit PATH, session-local HOME
and test-only PYTHONPATH if needed: no inherited endpoints, credentials or ZF_DATA.
Create `.copilot-tracking/.issue-108-tmp` under this worktree, pass its absolute
path as TMPDIR in every subsequent isolated application/test process and log
`tempfile.gettempdir()` before running. Remove this scratch directory after checks.
The historical Research baseline used default temporary directories; it remains
unchanged as original evidence rather than being relabelled.
Order: focused test_ai_eval first, full agents discovery, project-configured
Ruff/format/mypy, API test_ai_tasks, actual CLI --json written to a task evidence
path, parse/assert denominators/limitations and hash output. Run git diff --check.
Agent suite uses declared fixture helper paths; API tests use temporary JSON/
SQLite data and loopback HTTP only, no service SQL. Inspect runtime contract only
as direct pass-through; Docker/SQL service/Azure N/A, not passes. No inference.
Configured mypy/format exemptions are inherited and explicitly disclosed.
Completion: commands, exit codes, full failures, counts and SHA-256 receipts.
Actual: focused 13/13, agents 105/105, API 33/33; configured agents Ruff/format/mypy
pass, with inherited harness/test exemptions. Explicit API file formatting bypassed
its configured exclusion and failed; the untouched base also fails. Only the new
assertion block is formatted, and the configured force-exclude check skips the
legacy file honestly. No unrelated reformat. Offline JSON and console reconcile
14 priority results (eight AI/six template), ten priority scenarios and ten
scripted reviews; original quality/gate/claim boundaries retained.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Independent gate and publication

One fresh independent original reviewer receives source candidate hash, supplied
base, research/plan/details/changes/critique and entire actual diff, not merely
changed lines. Writes only original Review artifact. Preserve its complete
findings/verdict and SHA-256, even if adverse. No second original Review.
If required, correction receipts remain separate, maximum two source cycles.
Resolve gh api user before commits, local noreply author/committer and required
Copilot trailer. Conventional commits, normal push and main PR with Refs #108,
no closure keyword. All task artifacts committed, including state, plan,
details, research, critique, changes, original review and logs.
Reconcile published handoff, exact base/candidate/head boundaries and unmet
gates. If main moves, report it and await explicit coordinator integration
authorization; no rebase/force/merge. Final stop is coordinator exact-head
independent complete review, not actual-model acceptance.

Actual completion: original Review execution Complete, outcome Conformant with
justified divergence, RV-001 Low inherited checking residual and no introduced
defects. Source candidate a39ebe9755d07df23730ee81256c0c792fc0ff51; original Review
SHA-256 550efe3ad714778e7e378980cbf6643077d432212b3a63d81de244d477b496c1.
Normal topic push and main PR #405 executed. Final artifact-only delivery commit
retains identical source and immutable originals; no source corrections or second
Review. Exact publication head is pinned in PR metadata/final response. All
P01-P03 markers complete, no pending publication authorization. User-directed
stop is for coordinator's separate independent complete exact-head review.
