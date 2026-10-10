---
title: RPI Changes - Proper Warm Exercise PoC Rebuild
description: Local implementation evidence and unmet acceptance gates
ms.date: 2026-10-10
---

## Metadata

* Task ID: exercise-poc-rebuild-2026-10-10
* Plan: .copilot-tracking/plans/2026-10-10/exercise-poc-rebuild-plan.md
* Details: .copilot-tracking/details/2026-10-10/exercise-poc-rebuild-phase-details.md
* Declared scope: full plan, local implementation; live acceptance explicitly blocked.

## Execution Status

Partial against the complete accepted PRD. P01-P04 complete. P05 has a connected
local home-to-financial-closure implementation, but complete handoff/update and
fixture contracts remain outstanding. P06 local checks executed; complete
workloads/live/human acceptance and publication remain open. No full end-to-end
acceptance or conformant outcome is claimed.

## Completed Work

### Accepted baseline and reusable contracts

P01/P01-T01: PR #57 merged as 5a6ec60 after exact-head checks. New unpublished
rebuild branch based on merged main. Existing suite ran 270 tests in 44.766s:
OK, 26 live MSSQL tests skipped. No runtime or model success inferred.
Source and bounded planner assessment establish private geography exclusion,
reusable controls/SQL, missing forms/Decision/forecast and eleven/nine-path gaps.

### Domain, provider and fixture contracts

P02: forms.py/test_forms.py implement source-bound text/CSV extraction,
versioned six-template registry, field/protected-human reviews, calculations,
pack export and exact invalidation; 24 local tests passed.
P03: decision.py, decision_tasks.json, test_decision.py implement dedicated
transport/registry/proposal validation and reusable fail-closed guard;
25 fake-only tests passed; conservative provider response shape awaits probe.
P04: exercise.py/forecast.py, manifest/oracles and tests implement wholly
fictional fixtures, six scenarios, independent forecast/sensitivity oracles
and separate scale stream; 19 tests passed. Combined 68 tests passed.
P05: isolated factory/projection, usable labelled source evidence, common
generation guard/provenance, service/UI form reviews, separate financial events,
independent capacity/quality/milestones and cash/invoice closure integrated.
Ten connected integration tests cover the one-home journey, sibling isolation,
source/version invalidation, denied shortcuts, zero-call inference and rejected
application attempt chains. Evidence-support screening minimizes sources to
current field candidates and never approves a field. Unknown template/rule
versions block export; restoring versions preserves stale reviews.

Narrow data contracts add literal-text XLSX preview, at most 25-case coordination
bulk preview, fingerprint-bound explicit commit, idempotent retry/per-row outcomes
and role-projected JSON cohort/history export. Seven tests passed. This is not
arbitrary Excel, authoritative stock ingestion or XLSX full-history export.

P06: Chrome 152.0.7977.75 browser runner passed 22 finite checks, covering eleven
orientation profiles, nine workflow navigation entries, parser conflict,
320/390/1280px form reflow, root text resize, focus/labels/IDs and runtime errors.
The first browser run exposed real narrow-header overflow, fixed by wrapping
navigation/card content and labelled focusable scrolling tables. CSP remained
unchanged; test code was fixed to respect it.

Runtime runner took 200 warm HTTP samples each for list/detail/dashboard/write,
all below their individual thresholds, on one session/writer and 18 fictional
homes. Clean restart retained the exact case; SQLite backup/restore retained
the exact case and audit head. These are not prescribed concurrency/30-minute/
600,000-event scale or crash/RPO/response-loss drills.
The container now copies required evals/registry. Image build and non-root,
read-only exercise startup with writable state pass.

## Implementation-Time Plan and Detail Updates

One final-candidate critique returned Revise. Five compatible planner
corrections added common inference guard, external hazard authority,
generative provenance, actual text/CSV extraction and isolated exercise startup.
All are in the current plan/details; no repeat critique or owner question
needed. Runtime addition ceilings and zero test removals preserved.

## Validation Record

| Check | Scope | Result | Evidence |
| --- | --- | --- | --- |
| Baseline unittests | Existing MVP | Pass | 270 tests, 26 live SQL skips |
| Live Decision 1 and narrative | Required platform evidence | Blocked | No Decision deployment; billable/terms/cost authorization unverified |
| Integrated full suite | Local regression | Pass | 355 tests, 26 live MSSQL skips, 65.989 seconds |
| Changed JavaScript and whitespace | app.js, panels.js, exercise.js and Git diff | Pass | node --check; git diff --check |
| Browser orientation/parser/reflow | Finite engineering checks | Pass | exercise-poc-rebuild-browser-results.json, 22 checks |
| Sampled HTTP/clean backup | One session/writer; 200 samples/operation | Pass | exercise-poc-rebuild-runtime-results.json |
| Container startup | Non-root/read-only plus temporary writable state | Pass | Locally built image includes fictional fixtures/registry |
| Full PRD runtime acceptance | Complete accepted contract | Not run/Blocked | exercise-poc-rebuild-acceptance.md covers every FR/AC/NFR and known gaps |

## Blockers

Actual Decision 1 deployment/access/terms/costs and bounded billable authorization.
Human-adjudicated evaluation labels, paired-effort participants and real UX.
They block corresponding acceptance, not local exercise implementation.

## Remaining Work

P05 complete handoff/update/return/fixture acceptance contracts and P06 prescribed
workloads, failure/RPO/accessibility, actual models and human evaluation.
Current branch publication follows one independent review. No completed
full-PRD or observed-benefit claim.

## Pre-Review Reconciliation

Ready for a bounded review of implemented local changes and a complete
requirements-gap assessment, not for a conformant full-PRD verdict. Plan
P05/P06 markers intentionally remain unchecked. Details/state/evidence agree
on partial delivery and blocked live acceptance. Original critique retained.

## Follow-Up Items

None outside the current plan.
