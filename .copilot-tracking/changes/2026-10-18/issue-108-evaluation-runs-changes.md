---
title: Issue 108 evaluation run accounting changes
description: Source, validation and delivery evidence with explicit limitations
ms.date: 2026-10-18
---

## Metadata

Task ID 108; slug issue-108-evaluation-runs; implementation date 2026-10-18.
Exact base: 69091f4149f2fd217fc33a8c965ebcb6d5064956.
Plan: .copilot-tracking/plans/2026-10-18/issue-108-evaluation-runs-plan.md.
Details: .copilot-tracking/details/2026-10-18/issue-108-evaluation-runs-phase-details.md.
Branch: fix/evaluation-run-accounting-108 in isolated caller-supplied worktree.

## Execution Status

Full bounded plan complete: Research, Plan, Implement, one original independent
Review and normal branch/main-PR publication. All P01-P03 tasks complete.
PR: https://github.com/jmservera/ama/pull/405. Source candidate:
a39ebe9755d07df23730ee81256c0c792fc0ff51. Artifact-only final delivery commit
is pinned by exact HEAD in PR metadata/final response; it adds no source changes.
Source writes limited to harness, focused tests, narrow README
and one direct API contract assertion. No source correction cycle consumed.
No implementation blocker.

## Execution Summary

Research independently reproduced final-source-dependent undercounting.
The original one-time independent critique is Revise, one Medium PC-001.
Direct planner disposition adds verified task-local TMPDIR for all subsequent
isolated validation; original critique remains unchanged with hash
b6117e40523ce84c5c163d913263224abda62b8d40530e09fd6de4f5b33f1397.
This recipe change does not alter the original default-temp Research baseline.

## Implementation-Time Plan and Detail Updates

PC-001 is resolved in plan Non-Functional Requirements and details P03-T01.
No user intent, source contract or acceptance threshold changed. No second critique.
All subsequent test/application commands run with `env -i`, explicit PATH,
session-local HOME, worktree-local TMPDIR and only declared test helper imports.
Initial system-Python focused test failed with ModuleNotFoundError zava_forward;
only then an isolated venv was created and core/agents dev and API distributions
installed via pip. Existing focused baseline then passed six tests.

## Completed Work

### P01-T01: Behavioral red baseline

Seven focused test methods added to the existing owner, no removals.
Captured returned metadata, mixed orders/null fallback label, repeated templates,
five-output identity, final-only quality and early critical/citation failures
are exercised using existing constructed golden scenarios.
Before production repair: 13 tests run, two failures and six errors; failures
include the exact (2,1) instead of (2,2) AI-run defect, and errors show missing
run evidence/scope fields. Complete command/tracebacks/exit 1 retained in
.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-red.log.
No new dataset or test owner; PC-001 TMPDIR check executed successfully.

### P02: Canonical run evidence and direct contract

Harness now exposes ordered returned run metadata and both measured latencies.
Summary derives source counts and model/prompt sets from those records, while
preserving scenario-final quality and once-per-scenario scripted reviewer counts.
Review records bind the actual scripted owner and recommendation ID. Console
counts explicitly say not provider calls. Additive scenario counts distinguish
mixed membership from exclusive run totals. Agents README documents old
`ai_runs` correction and all denominator/quality/identity limitations. Direct
manager-only report API test asserts returned count reconciliation, without
server/runtime changes.

Focused after repair: 13 tests pass, exit 0. Evidence:
.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-focused.log.
No production gate, core runtime, golden fixture, dataset, registry or KB changed.
No post-Review source correction cycle consumed.

## Validation Record

Historical Research baseline: six focused tests passed and constructed reproduction
confirmed five outputs counted as one AI run; mixed orders report zero versus one.
Original log: .copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-baseline.log.
### Command environment and local results

All post-critique Python/test/quality executions use an empty inherited environment:

```bash
V=/home/azureuser/.copilot/session-state/c9d20e32-acb0-442b-b8a6-6ed95534cb8b/files/eval-venv
H=/home/azureuser/.copilot/session-state/c9d20e32-acb0-442b-b8a6-6ed95534cb8b/files
T=/home/azureuser/source/ama-wt/issue-108-runs/.copilot-tracking/.issue-108-tmp
mkdir -p "$T"
env -i PATH="$V/bin:/usr/bin:/bin" HOME="$H" TMPDIR="$T" ...
```

No inherited AI_ENDPOINT, AI_DEPLOYMENT, AI_MODEL_VERSION, identity endpoint/header,
Azure/OpenAI credential, ZF_DATA, ZF_AI_GOLDEN or other service configuration.
The scripted adapter replaces `_chat`; no actual provider or identity token call.
Stores always use constructed temporary files. The red log proves resolved TMPDIR.
Initial missing-package command was system Python `-m unittest discover -s
src/agents/tests -p test_ai_eval.py -q` (exit 1, ModuleNotFoundError). Only after that:
`python3 -m venv "$V"` and `"$V/bin/pip" install --quiet -e 'src/core[dev]'
-e 'src/agents[dev]' -e src/api` (exit 0). No manifests changed; no uv.

| Command under isolated prefix | Result | Evidence log suffix |
| --- | --- | --- |
| Root: python -m unittest discover -s src/agents/tests -p test_ai_eval.py -q, before repair | Expected failure: 13 run, two failures/six errors, exit 1 | red.log |
| Same focused command after repair | 13 passed, exit 0 | focused.log |
| src/agents: python -m unittest discover -s tests -q | 105 passed, exit 0 | agents.log |
| src/agents: ruff check . && ruff format --check . && mypy | Pass; 19 formatted files, 23 mypy source files, exit 0 | quality.log |
| src/api: python -m unittest discover -s tests -p test_ai_tasks.py -q | 33 passed, exit 0; includes JSON/SQLite, negative controls and loopback HTTP | api.log; api-final.log |
| src/api: ruff check tests/test_ai_tasks.py | Pass, exit 0 | api-quality.log; api-final.log |
| src/api: ruff format --check tests/test_ai_tasks.py | Failed, exit 1, explicit path bypasses inherited formatter exclusion | api-quality.log |
| git show supplied-base:src/api/tests/test_ai_tasks.py piped to ruff format --check --stdin-filename tests/test_ai_tasks.py - | Same pre-existing formatting failure, exit 1 | api-format-baseline.log |
| src/api: ruff format --check --force-exclude tests/test_ai_tasks.py | Configured exclusion, no formatting coverage claimed, exit 0 | api-final.log |
| Root: python -m zava_forward.agents.ai_eval --json | Offline report, exit 0 | offline-report.json |
| Root: python -m zava_forward.agents.ai_eval | Explicit count console and claim limitations, exit 0 | console.log |
| Parse offline JSON and assert exact denominators, per-run identities, unchanged quality/claims | Pass, exit 0 | reconciliation.log |
| git diff --check | Pass | local command |
| git diff --exit-code supplied-base -- docs src/core src/agents/evals .github/workflows | Pass: protected paths byte-identical | local command |

All evidence paths share prefix
`.copilot-tracking/reviews/logs/2026-10-18/issue-108-evaluation-runs-`.
Agents discovery adds absolute PYTHONPATH of src/agents/tests and src/core/tests.
API selection adds absolute src/core/tests and src/agents/tests; no mvp path.
The API assertion block was formatted without reformatting the legacy file,
then the actual API tests/lint were rerun successfully in api-final.log.
Agents configured formatter and mypy exempt the migrated harness/focused tests;
these are existing limitations, not strict harness type/format acceptance.

The JSON/console show eleven total report results, ten priority scenarios,
14 priority recommendations = eight AI-sourced scripted outputs + six
template/fallback outputs. Reviewer counts stay eight accept/one edit/one reject,
with final recommendation IDs and scripted owner identity. Critical misses zero,
citation validity 74/74, final-scenario mean overlap .9, Spearman .722 and
recall differences .25 match the pre-change baseline. Those recall differences
are constructed fixture measurements, not incremental benefit.

### Immutable input and candidate fingerprints

| File | SHA-256 |
| --- | --- |
| src/agents/evals/ai_priority_golden.json, unchanged | 45c5762bbece1ff5604ea51ee6408e82f0ae5576d17cae8a4c925991c1610d5b |
| src/agents/src/zava_forward/agents/ai_eval.py | 9101bef9f27c3a79d87d4eb2dcbb9683bd822a9ff00a00ed2c9b7d94e55b16e5 |
| src/agents/tests/test_ai_eval.py | 0f0c7935043152c623d70ee4fc52b93a9b108e0128de465e1bdc9d4fcf1b4cea |
| src/api/tests/test_ai_tasks.py | e05240b1a4d61357def93a5b4d2eab7e62807128ae2e73612a2a7caed2a32c58 |
| src/agents/README.md | 7cd9c4482b83354428af56f6ac9bf66fd6e0b308730b47eb6bbc9c1374d81865 |
| Offline JSON report | b89eaf3d50ecc43365d71a6e92f53cd8b9f9986d1698eb06103edec8f6258192 |

Source candidate commit: a39ebe9755d07df23730ee81256c0c792fc0ff51. Original
Review assessed its complete 22-file base-to-candidate diff/artifact boundary.
The final artifact-only delivery commit contains this receipt, the unchanged
original Review and reconciliation; its hash is pinned in PR metadata/final
response because a commit cannot contain its own hash.

### Checks not performed

Service SQL, Docker/image, Azure, IAM, deployment and actual inference are N/A
to this offline report-accounting patch, not passes or CON-009 acceptance.
No runtime store/API implementation changed; the direct API pass-through
contract is exercised locally with JSON/SQLite and loopback HTTP only.
No held-out/human/cohort/approved-threshold/real serving/usage/cost study ran.
No calibrated benefit, model selection, release or whole-issue acceptance.

## Pre-Review Reconciliation

Historical handoff was ready: P01/P02/P03-T01 checked with matching evidence,
P03-T02 explicitly reserved for Review/publication, not incomplete source work.
Original Review has now executed once, Complete, Conformant with justified
divergence. Independent reviewer assessed all 22 candidate files and reran
focused 13, agents 105, API 33 plus configured quality/base negative controls.
RV-001 Low is inherited static-check coverage, not an introduced defect.
No source corrections or second original Review. Original Review SHA-256:
550efe3ad714778e7e378980cbf6643077d432212b3a63d81de244d477b496c1.
All current plan/details/status markers are complete and reconcile with actual
PR #405 publication; no stale pending publication authorization remains.

## Blockers and Remaining Work

No blocker or active task remains for bounded offline accounting/publication.
Coordinator independent complete exact-final-head review remains a separate
explicit owner boundary, not performed or presumed accepted by this original Review.
Remote main observed at supplied base 69091f4149f2fd217fc33a8c965ebcb6d5064956.
No integration/rebase/merge/force-push authorized or performed.

## Follow-Up Items

Coordinator exact-head independent complete review and explicit authorization
for any main integration remain separate. Issue #108 actual-model, held-out,
human, threshold, comparative effort/cost, serving usage/version, unknown liability,
region/quota, finite authorization and provider/privacy/consent gates remain unmet.
Real AI/SQL/Azure CON-009/AC-057 acceptance is not supplied by this offline fix.
RV-001 Low is routed to the existing migration-quality owner for separately
authorized exemption work; no new issue or broader reformat was created.

## Publication and Final Boundary

User explicitly authorized commit, normal branch push and main PR. Authenticated
account resolved with gh api user: id 8036360, login jmservera; repository-local
author/committer email 8036360+jmservera@users.noreply.github.com. Required Copilot
trailer retained. No private/global email, amendment, force-push, rebase or merge.
Normal push and gh pr create produced PR #405. Follow-up artifact-only commit
delivers original Review, all current phase/state reconciliation and delivery
receipt, preserving exact source candidate and original adverse evidence.
The final boundary is enumerated in the delivery receipt. Existing upstream
403/404 src and KB, issue #122 and held #92 are untouched.
No issue/board writes, closure keywords or acceptance checkbox changes.
Stop after final normal push for coordinator complete independent exact-head review.
