---
title: Issue 176 recovery implementation evidence
description: Fresh inspection and execution, distinct from unavailable historical logs
ms.date: 2026-10-17
---

## Invocation Scope and Opening State

Task 176, synthetic-determinism-176. Recovery plan P01 inspection/validation;
P02 Review and publication follow in order under the explicit user request.
Starting head: `196972dc0dac256cdfd41f70bc06e7cad5fbebf2`.
No application changes planned; only new dated recovery tracking evidence.
Research, plan verification, implementation inspection and recovery Review
performed now in order. Original 2026-10-16 artifacts remain unchanged
historical inputs. Validation/inspection complete and passing; evidence
publication verified below. No private data or default generator run permitted.

## P01-T01: Implementation Inspection

Complete. Read the exact feature diff, full stock_fabric.py and
test_stock_fabric.py, provenance.py, synthetic/__init__.py, data_paths.py,
all four selected test modules and related documentation changes.
Strict parse_as_of executes before input reads/writes; nullable as_of only
updates the summary. Each raw input is read once and the same bytes are
hashed and decoded. StringIO(newline="") preserves prior utf-8-sig CSV
semantics; cases retain utf-8 JSON/history semantics. Logical digest keys
contain no paths/content and absent cases produce no fabricated digest.
The existing v1 algorithm, row order, defaults, output guard and source
revision dependencies remain unchanged.

PC-002 assertions exist for BOM/quoted CRLF, independent raw-byte changes
without payload drift, date-only payload equality, read-once spies, omitted
cases, invalid-date no-write and full nonempty-destination preservation.
PC-001 remains the explicit Review disposition gate. No genuine introduced
bug found; no application or test changes made.

Safety inspection: generated-dataset and connected 60,000-home tests patch
builder.load_register; all selected outputs/SQLite files are temporary.
The existing fictional scale regression is not a new continuing-stock
replacement and proves no original OSM stock reproduction.

## P01-T02: Fresh Validation

Initial system-Python command:
`cd src/core && PYTHONPATH="$PWD/tests" python3 -m unittest -q test_stock_fabric test_synthetic_determinism test_sensor_stock test_generated_dataset`.
Exit 1: four module import errors, each `ModuleNotFoundError: No module named
'zava_forward'`; no selected test body executed. This is a missing install,
not a source regression or four meaningful test cases.

Created exclusive owned venv `/tmp/ama-176-recovery-20261017-xGWcVW` after
that missing-dependency failure. `python3 -m venv` and
`<venv>/bin/python -m pip install --quiet -e './src/core[dev]'` both exit 0.
No uv, dependency-manifest changes or extra runtime dependencies.
Python 3.12.3; declared Ruff 0.17.1 and mypy 2.4.0 installed with pip.
Fresh scoped tests and whole-core lint/type checks completed:

| Check | Fresh result | Durable direct output |
| --- | --- | --- |
| Four named unittest modules, `-v` | 45 tests passed, no skips, 10.154s, exit 0 | `.copilot-tracking/changes/2026-10-17/synthetic-determinism-176-tests.txt` |
| Whole-core `python -m ruff check .` | All checks passed | `.copilot-tracking/changes/2026-10-17/synthetic-determinism-176-lint.txt` |
| Whole-core `python -m ruff format --check .` | 47 files already formatted | Same lint output |
| Whole-core `python -m mypy` | No issues in 100 source files | Same lint output |

Actual output was appended directly with `tee`, with pipeline failure
propagation and explicit exit codes, not transcribed from old `/tmp` logs.
Historical standalone CLI smoke remains historical; current stock-fabric
tests include actual installed CLI subprocess replay/refusal checks.

## Amendments, Divergences and Follow-Ups

No behavior changes or scope expansion. Research corrected the historical
docs-only merge characterization and records the missing independent MERGE
receipt. Original generator and policy adoption gaps remain unchanged.

## Handoff

P01 complete and reconciled with plan/details; no source defects, amendments,
blocked validation or new implementation work. Ready for one recovery
Review. P02 Review is now complete; publication remains unchecked. Full issue acceptance is
still partial: original stock reproduction unavailable, historical manifests
unchanged and owner policy adoption unperformed.

## P02-T01: Recovery Review

One recovery Review performed after fresh execution: Complete / Residual
work. No introduced implementation defect found. RV-001 original stock
source/receipt gap and RV-002 policy adoption remain distinct follow-ups.
RV-003 records unavailable prior independent MERGE provenance, not a refuted
caller report or recovered approval. Historical docs-only merge claim is
qualified using actual diff evidence. No second Review or implementation
loop. Parent now owns authorized publication and final session stop.

## P02-T02: Publication Preparation

Direct git/current issue/PR/exact-head check evidence was captured in
`.copilot-tracking/changes/2026-10-17/synthetic-determinism-176-git-evidence.txt`.
Temporary venv `/tmp/ama-176-recovery-20261017-xGWcVW` was removed only after
checking its exact owned pyvenv.cfg/interpreter; absence verified. Test
TemporaryDirectory outputs are already cleaned. Persistent transcripts
contain only constructed-data execution and non-secret GitHub/git metadata.
No documentation/knowledge-base files changed during recovery, so no new
reference index/log update is necessary.

## Publication Verified and Closeout

Resolved authenticated `gh api user` immediately before commit, constructed
the returned ID/login noreply address and configured repository-local
user.email; author and committer explicitly used that address.
Conventional Commit with Refs #176 and required co-author trailer:
`551b99fe0b293ceeef0b59416236f04c48fe3181`
(`docs: record synthetic determinism recovery verification`).
Normal push succeeded on the existing branch. `git ls-remote`, local HEAD
and PR head all matched this full evidence SHA. PR #368 remained OPEN,
targeting main; body preserved and recovery appendix added, Refs #176 true,
closingIssuesReferences empty. Git diff against inspected head for
src/infra/docs/support/mvp/prototype/.env/.vscode empty; worktree clean.
Staged new-artifact `git diff --cached --check` passed before commit.

New hosted checks on the evidence commit were queued/in progress at that
verification, not claimed passing. Twelve SUCCESS checks belong to the
pre-recovery inspected head only. Final metadata-only closeout will be a
separate normal commit/push; final full HEAD is read from Git and reported
in the handoff rather than attempting an impossible self-referential SHA.
No Review repetition or new application/test execution is claimed.
Task recovery is complete; session stops as explicitly requested.
