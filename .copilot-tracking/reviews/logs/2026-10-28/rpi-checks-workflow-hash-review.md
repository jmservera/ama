---
title: RPI checks workflow hash independent Review
description: Original post-implementation Review of the bounded workflow pin refresh
ms.date: 2026-10-28
---

## Opening Review State

* Goal: assess P01 implementation and reconcile P02 pending publication against the supplied task, plan and critique.
* Scope: tools/rpi-checks.py, tools/test_rpi_checks.py and the canonical dated RPI artifacts; compare against origin/main at 98b0bb98f2424dd23c00e386378f44892a7a79e0.
* Evidence readiness: canonical research, plan, phase details, changes and critique paths located; substantive comparison pending.
* Acceptance basis: all WORKFLOWS pins checked, one raw SHA256 refresh, existing test extended, no workflow edits or .env access, tests and actual preflight; standing full gate and receipt verification before publication.
* First comparison boundary: P01 changes and validation versus plan markers, then P02 publication claims.
* Read-only boundary: only this review record may be written; no delegates, implementation, other artifact edits, commits, pushes or PR creation.
* Initial blockers: no review blocker identified; publication evidence remains to be assessed.

## Scope and Exact Assessed Boundary

* Task: rpi-checks-workflow-hash; original independent Review, 2026-10-28; no delegates.
* Branch: fix/rpi-checks-workflow-hash. HEAD and origin/main: 98b0bb98f2424dd23c00e386378f44892a7a79e0; assessed source is uncommitted.
* Complete tracked diff against that base: tools/rpi-checks.py and tools/test_rpi_checks.py only; 26 insertions, 2 deletions. Dated untracked evidence was assessed separately below.
* SHA256 of `git diff --no-ext-diff --binary origin/main -- tools/rpi-checks.py tools/test_rpi_checks.py`: b3c34aa7c47053246becfbd72c70268c821f9104f361cd00ece81999677dc5e1.
* No workflow edits; no .env access. This boundary is not a committed exact-head assessment or publication approval.

## Execution Status

* Review execution: Complete. P01 execution: Complete; full task execution: Partial because P02 publication remains pending.
* Compared the complete canonical artifact set, critique, source diff, existing test/preflight contracts, workflow history and publication policy.

## Reconciliation and Completed Work Assessment

* P01-T01: only test_matrix_drift_and_unreviewed_extra_commands_refuse extended; selector checks retained, real pin/key equality added, matched fixture passes, all five mutations require exact-name failures.
* P01-T02: one explicit deployment SHA256 changed to 3c2f1ed59b1486fc1316a48207cc4ef7d6a830bbba1dcad4152acab4bd2f1bbc; four matching pins and fail-closed production behavior unchanged.
* Independently hashed all five WORKFLOWS entries: every current pin matches raw bytes. src-deploy.yml alone differed at the base.
* Git f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc (#500) confirms exact-main source-CI prerequisite and per-image SPDX additions; 864a502126ee0dfedf13eaf54f08a10f2339279c (#480) already updated both CI pins and SQL selector.
* P02-T01 was accurately pending in pre-Review artifacts; this record supplies its one original outcome. P02-T02 remains active publication work, not an implementation defect or out-of-scope follow-up.

## Implementation-Time Updates, Critique and Follow-Ups

* Plan/details/changes reconcile P01 completion and pending P02 consistently; no significant or divergent decision, material scope revision or premature dependent work identified.
* Test fixture command rows correct the positive fixture's no-empty-evidence contract; the changes record preserves the initial mixed failure and subsequent sole-pin red run.
* Missing Ruff restoration followed an actual failure; initial noncanonical Ruff diagnostics remain disclosed, without unrelated fixes. Canonical checks and formatter adjustment stay within accepted scope.
* Original critique: Complete / Pass, no findings or unresolved dispositions; current implementation preserves its acceptance boundary. No fresh planning/critique needed.
* Plan Follow-Up Items: none; no implementation-discovered out-of-scope item requires a distinct follow-up owner.

## Validation Evidence

* Review-executed: independent AST extraction/raw SHA256 comparison of all five entries and exact key set, git diff --check, empty workflow diff, and merged workflow-history inspection: Passed.
* Implementation-reported, not rerun here: python3 -B -m unittest tools.test_rpi_checks -q: all 30 passed; red-before-green actual pin and five fixture negatives documented.
* Implementation-reported: real Runner.preflight passed Python 3.12.3, Node 24.21.0, Docker client/server, Bicep 0.48.1, actionlint 1.7.12, ShellCheck 0.11.0, Trivy 0.76.0 and every pin; no mocked real probes.
* Implementation-reported: Ruff 0.17.1 check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100, canonical format --check, and strict mypy 2.4.0 passed both files.
* Historical missing Ruff/noncanonical lint failures were not canonical final failures. Preflight logs are referenced in changes; external raw logs were not independently inspected in this Review.
* Complete --all gate, authoritative receipt verification, independent committed exact-head assessment, push/PR and hosted/human approval: not performed here; pending P02, not represented by preflight.

## Findings, Outcome and Routing

* Outcome: Conformant for completed P01 and P02 pending-publication reconciliation. No substantive RV findings; Critical 0, High 0, Medium 0, Low 0. Defects: none.
* Routing: no rpi-implement defect, rpi-plan decision gap, rpi-research material evidence gap or distinct residual-work item. Parent retains planned P02 continuation.
* Review blockers: none. Publication is not ready: commit source and original dated evidence with authenticated privacy-safe identity, Copilot trailer and Refs #500; run full --all to a new external directory.
* Fetch main and verify the authoritative receipt against current origin/main immediately before push; require separate independent exact-head assessment. Later commit/rebase/base/tool/image/input changes invalidate gate evidence.
* Missing prerequisites or failed checks block publication; no lighter-tier substitution, fabricated gate approval, protection bypass or merge authorization is granted.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/rpi-checks-workflow-hash-research.md](.copilot-tracking/research/2026-10-28/rpi-checks-workflow-hash-research.md) | Pin provenance and all-workflow research |
| [.copilot-tracking/plans/2026-10-28/rpi-checks-workflow-hash-plan.md](.copilot-tracking/plans/2026-10-28/rpi-checks-workflow-hash-plan.md) | Requirements and P01/P02 markers |
| [.copilot-tracking/details/2026-10-28/rpi-checks-workflow-hash-phase-details.md](.copilot-tracking/details/2026-10-28/rpi-checks-workflow-hash-phase-details.md) | Execution and publication contracts |
| [.copilot-tracking/changes/2026-10-28/rpi-checks-workflow-hash-changes.md](.copilot-tracking/changes/2026-10-28/rpi-checks-workflow-hash-changes.md) | Original validation and remaining work |
| [.copilot-tracking/reviews/plans/2026-10-28/rpi-checks-workflow-hash-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/rpi-checks-workflow-hash-plan-critique.md) | Original Complete / Pass critique |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Single raw pin and unchanged preflight |
| [tools/test_rpi_checks.py](tools/test_rpi_checks.py) | Existing test extension |

## Next Steps

Parent may record P02-T01 completion and continue planned P02-T02 gates/publication; preserve this original outcome. No second Review is requested.
