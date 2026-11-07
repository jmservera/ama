---
title: Issue 1231 review r6 (retained-stage wording accuracy)
ms.date: 2026-11-06
---

## Chronology and independence

Written after the r6 Changes record was complete, in its own call, about 14:15Z (estimate; the actual check run finished at 14:13:39Z). This is one author Review by the implementing session. It is not independent and not a feature or publication Pass.

## Artifact set

* Research, plan, details, critique (Pass, PC-001), changes under `.copilot-tracking/*/2026-11-06/issue-1231-r6-stage-wording-*`.
* Prospective commit `d4640358bd5ea7645bea04923a7c058246974a2d` (14:12:09Z) precedes both source edits.
* Source diff: two files, 4 insertions and 2 deletions, in `src/core/src/zava_forward/core/ranking_publication.py` and `ranking_publication_runner.py`.

## Assessment

* Requirements: both unconditional alias claims are gone (`grep "hard-link alias" src` empty). The docstring now distinguishes the committing writer's stage (shares bytes and inode) from a loser's never-linked stage (can differ). The runner warning is conservative ("may share the archived record's bytes, so do not edit it") with code, stage name, next action, status and keys unchanged. The remove-by-hand action is kept.
* Scope: no logic, outcome, key, error, date, audit, storage, README or test change; matches the plan. README never made the claim.
* Validation: 73 tests OK (publication, runner, API wiring), Ruff check and format exit 0, mypy from `src/core` exit 0 on four files. The root-invoked mypy attempt exit 2 was an invocation error and is preserved. Tracking blobs unchanged. Light, shared, unpinned environment.
* Divergences: none from the plan. The recorded estimated times in the Plan, Details and critique exceed the actual commit time; the Changes file states the commit time is authoritative.

## Findings

* RV-001 Low, residual. The wording is not asserted by any test; the loser regression covers behavior only. Intentionally not added (plan decision). Destination: none.
* RV-002 Low, residual. The runner warning is shown for both outcomes and cannot say which applies. Wording is conservative so it is accurate for both. Destination: none unless the owner wants outcome-specific text (distinct follow-up, not planned).
* RV-003 Info, carried. Evidence is light and shared-venv only; final combined FULL, independent whole-feature review, hosted CI and publication remain pending with the coordinator. Real unsupported-mount test remains an optional follow-up.

## Outcome

Execution Complete. Outcome Conformant for the r6 wording scope on light evidence, with residual items above. No material findings open.
