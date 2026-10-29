---
title: Bounded mixed-source lifecycle remediation
description: Subsequent implementation of original Review findings without repeating Review
ms.date: 2026-10-29
---

Task ID: 533-tie-remediation; parent 533-correction4.
Declared scope: P01 in matching plan/details. Bounded implementation complete;
source/evidence committed locally at 72cdda27 and session stopped.
Evidence: original Review Complete / Not accepted at 60004dde, unchanged.
Resolve RV-001 mixed-source tie ambiguity and RV-003 confounded fixture flags
within the user's full sibling-sequence correction scope. No repeated critique
or Review. RV-002 full/browser validation remains blocked; no heavy retry.

## P01 Execution

Persistent regressions first, source-aware tie reconciliation second, then
strict static and targeted fallback checks with local-only commit.

### P01-T01: Exact persisted regressions

Expanded only the existing methods in test_progress_dashboard.py; no additional
method/helper or removed assertion. The 30-cell table now sets closed=True for
A->T and C->T, so their illegality cannot be masked by a final snapshot mismatch.
New negative controls cover accepted/human/withdrawn/excluded closure and both
reopen sources at one timestamp across collections, both open and followed by a
later final closure. Mixed closing aliases and original identification evidence
at a shared reopen instant are also covered. Every constructed payload still
roundtrips exactly through JSON and SQLite before full lifecycle/dashboard/
archive assertions.

Retained red mixed-source evidence: 2 inherited methods / 24 failed subtests,
0.631s, mixed-source-red.log, before the ambiguity guard.
During the same bounded genuine-duplicate audit, distinct versions exposed
another direct aliasing case: same timestamp/kind but different recorded
observations. Added five same-kind version controls and repeated-human-closure
after-corroboration control. distinct-evidence-red.log retains 12 expected
failures in 0.728s before observation identity comparison.

### P01-T02: Source-aware ties and genuine observations

progress.py now carries collection provenance and raw observation through
extraction. Equal-instant groups with multiple sources, opposing closes and
reopens, and repeated lifecycle evidence are unknown: source concatenation
cannot establish duplicate adjacency. Single-stream legal alternating episodes,
plain duplicates, closing corroboration and isolated cross-source close/reopen
remain known.

Replay also compares the remaining observation fields for same-kind/time
duplicates, not just the target boolean or kind. Timestamp spelling is excluded
after observed() normalization, preserving timezone-equivalent duplicates.
Distinct versions or differing fields are not erased. Corroborating closing
kinds are retained per current transition, so a later distinct observation of
the same closing kind cannot hide behind an earlier accepted-handover row.
Observation identity is reset after every lifecycle-changing transition.
No schema, producer, dependency, generic replay framework or override added.

API README qualifies same-instant preservation by evidenced collection order
and documents unknown mixed-source ambiguity and distinct observation identity.
No core/web/pinned dataset files changed.

### P01-T03: Validation

Same external evidence root as the parent:
/tmp/ama-533-correction4-20261029. No heavy admission retry, lock polling,
shared environment mutation, full suite or browser command was performed.
Existing /tmp/mv mypy/Ruff and /tmp/ama-533-venv runtime use absolute worktree
src/test PYTHONPATH as in the original correction.

| Check | Actual command / scope | Result / retained evidence |
| --- | --- | --- |
| Mixed-source red | Two inherited review-counterexample selectors | Expected 24 failed subtests; mixed-source-red.log |
| Distinct-observation red | Same selectors after source-provenance guard | Expected 12 failed subtests; distinct-evidence-red.log |
| API types | /tmp/mv/bin/mypy from src/api | Passed 102 files, exit 0; remediation-api-mypy-final.log |
| API lint | /tmp/mv/bin/ruff check . from src/api | Passed, exit 0; remediation-api-ruff-final.log |
| API format | /tmp/mv/bin/ruff format --check . from src/api | Passed 54 files, exit 0; remediation-api-format-final.log |
| Core types | /tmp/mv/bin/mypy from src/core | Passed 156 files, exit 0; remediation-core-mypy.log |
| Core lint | /tmp/mv/bin/ruff check . from src/core | Passed, exit 0; remediation-core-ruff.log |
| Core format | /tmp/mv/bin/ruff format --check . from src/core | Passed 103 files, exit 0; remediation-core-format.log |
| Final targeted regression | python -m unittest test_progress_dashboard test_workbench test_role_screens test_workspace_scripts test_taskqueues test_scenario_manifest -q | 77 passed, 15.580s, exit 0; remediation-targeted-final.log |
| Return guard sensitivity | Isolated in-memory source mutant removes only the return-open precondition, then runs the inherited 30-cell matrix | Exactly A->T/C->T fail in each backend (four expected failures); harness assertion passes, exit 0; return-guard-sensitivity.log |
| Full API/core and browser | Not launched after parent's busy admission | Still blocked, not replaced by targeted evidence |

An intermediate API Ruff run found a new 101-character test line. It was
formatted with the existing formatter; the original failed log remains, and
the final checks above pass with no suppressions. The final source and test
batch was validated after all edits. The isolated mutation probe alters no
tracked file and is test sensitivity evidence, not a second RPI Review.

## Plan/Detail Updates and Reconciliation

Directly applied RV-001/RV-003 within the user's complete correction scope,
using the original Review as adequate evidence for later bounded implementation.
The observation-version audit is immediately relevant local refinement of
genuine duplicate semantics; plan/details now name it and all added red evidence
is retained. No divergent decision, new authority, separate critique or Review.
P01-T01/T02/T03 complete; source/evidence committed locally at 72cdda27.
Original Review remains Complete / Not accepted at immutable source 60004dde.
These later changes do not assert independently reviewed closure of findings.

## Remaining Work and Follow-ups

No remaining active implementation task. RV-002 full/browser
validation remains an acceptance gap for later explicit coordination. No fresh
independent acceptance, publication receipt, hosted/human approval, push or
Azure action is claimed.

## Local Closeout

Original implementation/evidence commit:
60004dde5b1983d74f6b17faa69f509aead36569.
Subsequent source/original Review/remediation evidence commit:
72cdda2774c64510aea88c1ac4fddc570fcaa346.
Final closeout commit updates dated evidence and stopped-session state only.
Mode manual, current phase Follow-up, bounded task execution completed,
session stopped as the user requested. No automatic child work, second critique,
second Review, lock retry, push, force-push, merge, az or publication gate.
The original Complete / Not accepted review at 60004dde remains unchanged;
later source changes are scoped-tested, not freshly independently accepted.
