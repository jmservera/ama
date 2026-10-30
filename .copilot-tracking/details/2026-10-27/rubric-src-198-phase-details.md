---
title: Rubric src cut-over phase details
description: Implementation boundaries and evidence by task
ms.date: 2026-10-27
---

## Metadata

Task 198 / rubric-src-198. Plan:
.copilot-tracking/plans/2026-10-27/rubric-src-198-plan.md.
Research: .copilot-tracking/research/2026-10-27/rubric-src-198-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete: 31 targeted checks pass | P01-T01, P01-T02 |
| P02 | Complete: docs and validation reconciled | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Regression coverage

Source production semantics are already correct. Existing tests import a
changing score file or assume retired event paths. Keep tests outside packages,
change no app code, fixture failures must expose real regressions.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Stable baseline and event contracts

Gate tests need A2=5, A4=1, B3=1 and total 66 to prove specific drop/increase/
closed-criterion assertions. Use explicitly synthetic scores, not current
recorded 77. In prepare deletion test set a synthetic A2=5 workflow baseline, recompute its
total and sections, derive proposed scores from that baseline and submit A2=3.
Assert valid=true, passed=false, drops=[A2], removed path and expected total
baseline minus two. Runtime workflow tests must enumerate exact event sets:
source CI {pull_request, workflow_dispatch}, legacy/deploy {workflow_dispatch},
infra {workflow_run}, rubric {pull_request, push, workflow_dispatch}. Use src
source paths and keep names unchanged.
Completion: no seed/trigger failures; real-runtime missing prerequisite skips
remain visible.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Retired paths and trusted registry

Add one parameterized test function covering retired module, test, web,
Dockerfile, README and prototype deploy paths. Real temporary Git tests must
show no changed artifacts/criteria under the current registry. Add one
transition test: commit an old registry including mvp, remove evidence and
edit registry on feature, compute PR state from main, observe removed file;
first record the nonempty pre-delete solution-code fingerprint under the old
registry on main. Assert bootstrap=false, instrument_changed=true, all 20
criteria open, solution-code changed and the exact removed/changed path;
merge, then compute current state using merged registry and prove retired
membership absent and no retired removal under the merged registry, without
requiring should_score=false against the old fingerprint. Use synthetic text
only; no private data.
Completion: exact state assertions and all src/exclusion tests pass.

<!-- rpi:phase id=P02 -->
## P02: Evidence, validation and publication

Do not rewrite historical sign-off rows or PR bodies. Add later dated
reconciliation to the existing cut-over pack and index/log.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Durable record

Replace stale present-tense rubric MVP narrative with clearly historical
registry chronology and current src guidance; qualify prototype activation
advice as historical. Record 47 baseline at 9261c5c (scored 80660e95), 47
carried snapshots for M1-M6/R1, 77 pre-retirement, 77 hosted #499 and current
77 at 09099ecd. Include seven solution criteria and dated URLs/SHAs.
Record sequence deviations and absent fresh historical scores. Recovery matrix:
A1/A3/A4/A5/A6/A7/B6 candidate src evidence and migration PRs, no invented
improved grade or promised acceptance. Historical tests: 19 -> 11 after #295,
now 18 reassessed; record actual after result. No version or score-file edit.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Exact local evidence and one Review

Use python3 -m pytest .github/rubric/scripts -q -ra; run new selectors and
git diff --check. Confirm workflow Markdown/lock, registry and rubric version
unchanged. Check changed local links. No application suite needed for
test/documentation-only scope. No --all or optional heavy gate, no deployments
or scorer dispatch. Preserve original critique and Review; remaining findings
route to follow-up, not a second Review or repair loop. Use privacy-safe local
identity, Conventional Commit plus requested trailer, ordinary branch push,
one draft PR with Refs #198 and candid acceptance table after Review.

## Completion Evidence

P01: 31 targeted checks passed in 3.34s. P02: full rubric suite 374 passed /
one unchanged deck-selection failure / seven missing-runtime skips in 42.04s.
Added local Markdown links/anchors, diff whitespace, production workflow/lock/
registry/rubric/score byte invariants and original log prefix passed.
All implementation tasks complete; publication follows Review. No human
acceptance box was ticked and no issue was closed.
