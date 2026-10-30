---
title: Rebuild teardown dependency phase details
description: Execution boundaries and evidence for the PR 511 ordering correction
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: pr-511-teardown-order-2026-10-30
* Task slug: rebuild-148-teardown-order
* Related plan: .copilot-tracking/plans/2026-10-30/rebuild-148-teardown-order-plan.md
* Evidence: .copilot-tracking/research/2026-10-30/rebuild-148-teardown-order-research.md, C1-C6.

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Correct and regress teardown dependency | Complete | P01-T01, P01-T02 |
| P02 | Validate, independently review and commit locally | Complete; local commit 574954e0 | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct and regress the teardown dependency

* Context: C1 reproduces the lexical tie; C2 establishes the actual managed
  Private Link target. C3 provides a reusable deterministic backend.
* Intent: delete profile before environment without modifying safety admission
  or inventory readback checks.
* Boundaries: one integer tier change; no graph, Bicep or local fixture expansion.
* Completion: failing-first evidence, passing profile/environment regression,
  dry-run ordering check and README contract.
* Unresolved items: none. Original critique Complete / Revise preserved;
  PC-001's asserted /tmp restriction is not present in the parent context and
  is rejected in the plan. Actual validation commands remain mandatory.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add failing-first ordering coverage

* Context: existing dependency tests omit the profile and WAF; C5 confirms the
  roundtrip fixture does not include either.
* Likely target: src/orchestrator/tests/test_rebuild.py.
* Build an intentionally unsorted inventory including app, job, profile,
  environment and WAF. Profile kind mixed casing verifies lowercased ORDER
  lookup; names may oppose expected ordering. Run forward and reversed inputs.
* Assert expected deletion_order, actual MemoryBackend.deleted order and empty
  final inventory. Extend existing dry-run test with profile/environment indices.
* Dependencies: local packages installed before test execution.
* Validation: test_rebuild.py fails before the priority fix specifically on the
  profile/environment order; record failures, not fabricated prior success.
* Completion evidence: original red output in the changes artifact.
* Exact removals: none; maximum one new method, one existing method extended.
* Completion: 2026-10-30 failing-first run executed 23 tests and exited 1 with
  three failures: the dry-run assertion (profile index 10, environment 9) and
  each of the two inventory permutations. No errors or unrelated failures.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Correct the profile tier and document the contract

* Target: rebuild.py ORDER entry for microsoft.cdn/profiles, 2 to 1.
* Keep the environment at 2; no need to change relative order of unrelated
  resource types or introduce a new comparator.
* Target: src/orchestrator/README.md source-only rebuild rehearsal paragraph,
  explaining managed Private Link origin consumer-before-target order.
* Dependency: P01-T01 failure preserved.
* Validation: focused test_rebuild.py passes; no other runtime changes.
* Completion: green regression and source diff match the approved single-entry
  change; no tracker paths in production comments or commit text.
* Actual evidence: focused suite now passes all 23 tests in 2.516s, exit 0.
  Runtime diff is exactly the one profile priority change. No safety,
  comparator, Bicep or fixture-count change.

<!-- rpi:phase id=P02 -->
## P02: Validate, independently review and commit locally

* Context: caller names /tmp/mv and all four component checks. Historical
  publication blockers remain outside this correction.
* Boundaries: no Azure, push, private data, full-release or issue-closure claim.
* Dependencies: P01 and available /tmp/mv.
* Completion: command evidence, reconciled original dated artifacts,
  independent Review and local Conventional Commit.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute component validation and reconcile evidence

* Initial environment failure: /tmp/mv import of orchestrator raised
  ModuleNotFoundError; pip show finds current pinned Ruff/mypy but core is
  editable from another worktree. Install current core and orchestrator.
* From src/orchestrator:

```bash
/tmp/mv/bin/ruff check .
/tmp/mv/bin/ruff format --check .
/tmp/mv/bin/mypy
PYTHONPATH=../core/tests /tmp/mv/bin/python -m unittest discover -s tests -q
```

* Tests use existing local synthetic fixtures. Record any opt-in skips and
  failures accurately. Do not equate SQLite/unit tests to real Azure deletion.
* Review Markdown/links and git diff --check; no new doc build.
* Reconcile plan markers, details, changes, deviations and blockers before
  independent Review.
* Completion: /tmp/mv packages now editable from this worktree; Ruff 0.17.1
  lint passes, format reports 11 files already formatted, mypy 2.4.0 reports no
  issues in 14 source files. Full suite runs 69 tests in 6.783s, OK, exit 0,
  no skips reported. git diff --check passes.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Execute one independent Review and persist a local commit

* Fresh reviewer reads plan/details, critique, source diff and validation
  evidence; original output goes to
  .copilot-tracking/reviews/logs/2026-10-30/rebuild-148-teardown-order-review.md.
* Require execution and outcome separately. Findings route later, not to
  another implementation/Review cycle within this task.
* GitHub account readback returned id 8036360/login jmservera. Construct the
  privacy-safe email from actual returned values, configure repository-local
  user.email and use for both author and committer.
* Commit only source/test/README plus this task's dated artifacts; Conventional
  Commit with Refs #148 and required Copilot coauthor trailer.
* No push, merge, amendments, historical artifact rewriting or Azure.
* Check the persisted commit and clean task worktree after committing.
* Publication: full current-base local gate, exact-head assessment and
  human/hosted gates remain separate; no receipt or publication claim here.
* Completion: independent Review execution Complete, outcome Conformant,
  no findings. Local implementation and original dated RPI evidence persisted
  in 574954e0 with the required Conventional Commit and Copilot trailer.
  Authenticated GitHub privacy-safe email used for author and committer.
* All plan tasks complete. This administrative completion record follows the
  real commit; it does not rewrite the original Review or imply a repeated
  assessment. No push or Azure access.
