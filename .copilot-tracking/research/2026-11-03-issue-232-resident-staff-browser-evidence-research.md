# Research: issue #232 resident-staff browser evidence

* Disposition: executed (desk and repo inspection, 2026-11-03)
* Planning Readiness: Ready

## Delivered by merged PRs (do not redo)

* #652: resident-choice screen (measure and version choice, pause or withdrawal panel, linked update commitment with purpose, owner, due, safe route).
* #715: queue-level summary on the choice screen; repaired role-screens.js.
* #777: resident-service-issues screen (access needs, owners, linked commitment). Closed #487 superseded by these.
* #769 (issue #231) added the keyboard and axe pattern for technical and quality queues only.

## Gap found

* `src/api/checks/role_screens_browser_check.py` runs the shared keyboard, text-state and axe checks only for stories 231, 231q and 226. Stories 232 (choice) had phrase checks only; the service-issue screen had no browser check at all. Criterion 4 (keyboard and textual state evidence) is therefore unproven for both screens.
* Server-side cross-home queue projection remains unbuilt and is a larger slice.

## Slice chosen

Extend the browser check with story 232s and apply the accessibility checks to 232 and 232s. Test-and-evidence only, synthetic data, no product code change, no security, infrastructure, SQL or deployment surface (focused tier).

## Constraints kept

Read-only, no resident contact, human approval and consent boundaries unchanged; no AI feature is touched. Desk research, not observed behaviour; people and assistive-technology validation stays in #155.
