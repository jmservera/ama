# Plan: issue 954 photo flag browser validation (2026-11-09)

Task `issue-954-photo-validation`; research `.copilot-tracking/research/2026-11-09-issue-954-photo-validation-research.md`; details `.copilot-tracking/details/2026-11-09-issue-954-photo-validation-details.md`.

Tier: owner-selected DEMO targeted. Selected checks: the recovered browser checker, `test_photo_availability`, Core `test_scenario_manifest` and `test_needs_inventory`. No `rpi-checks --all`, no full matrix.

## Phases

* [ ] Phase 1: recover `src/api/checks/photo_flag_stale_browser_check.py` from `chore/photo-service-evidence-audit-954` (`1dc30f39`) by `git show` after this plan is committed; record its recovered blob identity.
* [ ] Phase 2: adapt only the checker to the clarified criterion and current main (no toast, no disruptive application error, no full reload, native diagnostics recorded separately and unfiltered, denials never turned into successes, own receipt written to scratch).
* [ ] Phase 3: run ruff check and format check first, then the checker (per status 503 and 403) under the heavy lock with worktree-bound imports; then the three targeted unit selections. Raw producer exits and logs stay outside the repo.
* [ ] Phase 4: review the one changed file against the freshly fetched web guidelines (checker only; no web asset edit). Record the outcome and correct only reproduced defects inside the correction budget.
* [ ] Phase 5: changes record, review record, state, handoff; commit; freeze.

## Boundaries

* No product (`app.js`) change unless a scoped bug is reproduced; if one is, stop that correction, record evidence and return it (budget 0 of 5 spent; no reset or extra grant is inferred).
* Preserve old branch `chore/photo-service-evidence-audit-954`, its adverse review and the 2026-11-07 observation unchanged.
* If the manifest recipe binding changes, update the existing recipe SHA and run its integrity tests; it is not expected to change.
* Acceptance box is not ticked by this lane; PR wording will be `Refs #954` unless every criterion is proven and integrated.
