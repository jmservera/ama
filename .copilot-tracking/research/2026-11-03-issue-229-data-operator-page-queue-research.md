# Research: issue #229 slice 4, page-level conflict and return queue

Disposition: reused (slice 1 to 3 evidence adequate; re-read of merged code). Planning Readiness: Ready.

## Delivered so far (merged)

* #654: per-home read-only Data steward and operator view. #779 and #819: browser check, keyboard, axe, reopened reason, fail-on-skip. #793: preserved artifacts. #493 closed unmerged.

## Gap found

Criterion 1 asks for a conflict and return queue. The merged view only shows one selected home; other role screens (hazard, choice, service) add a page-level summary across homes. The data screen had none, so a steward must open each home to find conflicts.

## Smallest slice

Add `summarise` and `summary` to the data-operator screen in `src/api/src/zava_forward/api/web/role-screens.js`: both source values with provenance, non-forward returns and reopens, unavailable homes listed, explicit "not a portfolio total" and "no winning source" text, no controls. Unit test only plus existing browser check run.

## Limits

Desk-based hypothesis. Not security, infrastructure, SQL or deployment: focused tier, no gate. No assistive-technology or human acceptance (#155, #151); Fluent adoption (#150) unchanged.
