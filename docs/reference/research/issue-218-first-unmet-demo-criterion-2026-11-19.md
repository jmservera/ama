---
title: Epic 218 first unmet demo criterion, no-retaliation proof for a signed-in principal
description: Selection of the first unproven child criterion under epic 218, an offline regression test for the live-shaped staff identity, and a per-criterion proven or unproven table
author: AMA RPI agent
ms.date: 2026-11-19
ms.topic: reference
---

Refs #218, #220. Scope: synthetic desktop demo under the owner decisions of 2026-11-18. Nothing here is resident, production or legal evidence.

## Selection

Open children of epic #218 are #220 to #224. The first unticked child criterion is #220 criterion 5, "No retaliation, inferred refusal or delayed hazard response". The [fourth live run](./issue-220-live-r4-challenge-route-2026-11-18.md) could not observe a successful staff-recorded write because the deployed image refused it with 403. The [identity fix note](./issue-130-identity-403-live-2026-11-18.md) describes the cause. Main already compares only email, code and oid (commit `e91b6fa81`), so the r4 statement that main holds no fix is out of date; the deployed image (digest `sha256:5368f4e4...`, revision 0000033 created 2026-11-18T22:39Z) still predates it.

## Change

`src/core/tests/test_challenge_signed_in_principal_220.py` (tests only, no behaviour change):

* A bound Entra principal (extra `tid`, `bound`, display name, derived keys) records a `nomination_record` step. Afterwards stage, hazards, closed, score, urgent and the portfolio ranking equal their values before the write, and exactly one record exists.
* A principal for a different object id is refused before any write.

Mutation probe: restoring the whole-dict comparison makes the first test fail with the live message "Reload your current staff identity before recording this step."; with the key comparison both pass.

## Validation (focused tier)

* `PYTHONPATH=src:tests python3 -m unittest test_challenge_signed_in_principal_220 test_issue_220_challenge_route test_no_retaliation_guard_220 test_nomination_route` in `src/core`: 26 tests OK.
* `ruff format --isolated --line-length 100 --check` and `ruff check --isolated --line-length 100` clean on the new file.
* `python3 -m mypy` in `src/core`: 22 errors in 3 files, all missing `opentelemetry` stubs in this environment; none in the new file. Unrelated to this change.
* No source behaviour changed, so the FULL tier was not triggered. `rpi-checks.py --all` was not run (heavy lock rule).

## Per-criterion table

| Criterion | Result for the demo | Basis |
| --- | --- | --- |
| #218 stabilization checkpoint (#440) | Unproven | Depends on open children and a checkpoint outside this task |
| #218 children closed or deferred | Unproven | #220 to #224 open |
| #220 no retaliation, inferred refusal or delayed hazard response | Proven offline for the live-shaped principal; unproven live | Test above; the deployed image lacks the fix and no image build or redeploy was done |
| #221 restart authority per RULE-024 | Not attempted | Next in order after #220 |
| #221 suspension and manual fallback drill (NFR-014) | Excluded for the demo | Owner decision: no drills |
| #222 owner approval of cohorts before live use (OQ-018) | Unprovable for the demo | Owner approval is a production matter; results stay synthetic |
| #223 all five criteria | Not attempted | Separate workstream |
| #224 four criteria | Deferred to production | #1905, owner decision 2026-11-18 |

The #220 criterion stays unticked: a real resident's experience of retaliation over time is production evidence, and the live observation needs a redeploy.
