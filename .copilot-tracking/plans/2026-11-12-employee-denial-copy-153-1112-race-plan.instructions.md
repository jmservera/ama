---
applyTo: '.copilot-tracking/changes/2026-11-12-employee-denial-copy-153-1112-race-changes.md'
---

# Plan: stale-stage advance refusal wording (issue 153 criterion 3, one path)

Research: `.copilot-tracking/research/2026-11-12-employee-denial-copy-153-1112-race-research.md`. Target: `feat/demo-ux-integration-1112` (stacked, unpublished). Details: `.copilot-tracking/details/2026-11-12-employee-denial-copy-153-1112-race-details.md`.

## Phase 1: regression first

* [ ] Add `test_stale_advance_refusal_names_owner_and_next_action` to `ApiTests` in `src/api/tests/test_mvp.py`: sign in as Sam, make ZF-3 advanceable (existing contract fixtures), advance as Pam over HTTP (200), advance again as Sam, expect `400`, error still starting "This case is not at the final checks.", containing "Owner: Sam Example" and "Next action: refresh the case and check its history", and no change to the case (stage stays "Install booked", one advance event). Run it and record that it fails before the source change.

## Phase 2: wording

* [ ] In `src/core/src/zava_forward/core/store.py` `Store.advance`, replace the stage-precondition message with: `This case is not at the final checks. It may have been moved on by someone else. Owner: {c['owner']}. Next action: refresh the case and check its history before trying again.` Nothing else changes: same `ValueError`, status 400, no replay, no client edit, no gate or permission change.

## Phase 3: validation

* [ ] Focused tests in the pip-installed venv: the new test, `api/tests/test_mvp.py`, `core/tests/test_content_standard*` and any test asserting the old text (none found by grep), ruff check and format on touched files, mypy on the api and core configured targets for touched files. Browser repeat of `/tmp/i153/race.py` to capture the rendered first-client message.
* [ ] Record changes, then one independent post-implementation Review with web-design-guidelines refreshed (no web file changed; rule applied: error messages include a fix or next step).

## Boundaries

No funding, role assignment, new approval, status semantics, automatic replay or refresh, client rewrite, lost server reason, or blanket filter. Preserve draft retention, stale-session suppression, duplicate prevention and history barriers (the client path is untouched).
