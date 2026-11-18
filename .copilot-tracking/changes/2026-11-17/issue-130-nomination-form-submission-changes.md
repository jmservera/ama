---
title: Issue 130 changes
ms.date: 2026-11-17
---

## Changes

* `src/api/src/zava_forward/api/web/nomination-routes.js` (new): submits the standalone acknowledgement, correction and challenge forms as JSON with `X-ZF-CSRF: 1`, shows the result in the existing `role="status"` feedback element, reloads on success.
* `src/api/src/zava_forward/api/nomination_routes.py`: loads the script with `defer`; challenge options carry `data-proposal-version` and `data-decision-version`.
* `src/api/tests/test_nomination_api_routes.py`: `test_standalone_route_forms_submit_in_browser` submits all three forms in headless Chromium (failed `[400]` on base).
* `src/api/tests/test_content_standard.py`: registers the new served script in the audited list.

## Findings during implementation (recorded, not hidden)

* The form `id` is shadowed by the hidden input named `id`, so `form.id` returned an element; the script reads the attribute.
* The correction route needs `challenge_id` present (null when none); the challenge route needs `proposal_version` and `decision_version`, which the standalone form never sent, so it could not have worked even with JSON. Versions are opaque strings.
* Editable install points `zava_forward` at the main checkout; tests were run with `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests` from `src/api` so the worktree code is exercised.
* Process deviation: an early fix attempt and the reproduction test predate the changes file; witness recorded "source already dirty at implement-start".

## Validation (FOCUSED tier)

* Base: new test failed with `[400]`.
* `python3 -m unittest tests.test_nomination_api_routes tests.test_content_standard` (src/api): 35 tests OK.
* `ruff check .` and `ruff format --check .` (src/api, project config): pass; `ruff format --isolated --line-length 100 --check` on the two nomination files: pass.
* `mypy` (src/api): no issues in 309 source files. `node --check` on the script: OK.
* Full `src/api` discovery was attempted once and truncated by the timeout; not claimed. `tests/test_fieldwork_variation_owner_guard.py` import error is pre-existing path-dependent (`test_procurement_api`).
* Not run: `rpi-checks.py --all` (FOCUSED tier; heavy lock held), axe/design-system browser harness, SQL.
