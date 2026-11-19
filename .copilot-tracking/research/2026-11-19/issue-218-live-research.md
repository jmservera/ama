# Research: epic #218, first unmet demo criterion (2026-11-19)

Task slug: issue-218-live. Base: 05e94d303. Scope: synthetic demo, desktop only.

## Disposition

Executed. Epic #218 has two unticked criteria of its own (stabilization checkpoint #440, children closed or deferred) that depend on the children. Open children and their unticked criteria:

* #220: "No retaliation, inferred refusal or delayed hazard response" (first in order)
* #221: restart authority per RULE-024; suspension and manual fallback drill (drills are excluded by owner decision)
* #222: owner approval of cohorts before live use (owner/production matter)
* #223: all five criteria
* #224: four criteria (legal review, deferred to production)

First unmet child criterion: #220 criterion 5.

## Findings

* Prior live note (docs/reference/research/issue-220-live-r4-challenge-route-2026-11-18.md): a staff-recorded write is refused 403 "Reload your current staff identity" because the deployed image (digest sha256:5368f4e4...) compares the whole Entra principal with the roster row.
* Main already holds `_same_signed_in_person` (email, code, oid only; commit e91b6fa81). The earlier note's statement that origin/main holds no fix is out of date.
* No unit test covers that function or a staff-recorded challenge write by a principal carrying extra Entra claims. The positive no-retaliation path for the live-shaped principal is therefore untested; existing tests use the roster row itself as the actor.
* Live revision ca-cutover-test-demo-api--0000033 still runs the same image digest, so the fix is not deployed. Redeploying an image is outside what this task will do (no image build authorised in the brief); live proof stays blocked.

## Planning readiness

Ready: add focused core tests for the live-shaped principal (positive no-retaliation write, ranking and hazard clock unchanged; mismatched code/oid refused).
