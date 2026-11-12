---
title: Issue 96 saved export check M1 correction 2 changes
description: Changes, failing-first evidence and validation for removing the broad TypeError fallback from the saved export check route
ms.date: 2026-11-12
---

## Changes

* `src/api/src/zava_forward/api/server.py`: deleted the `try/except TypeError` retry. Added `saved_export_ids_are_text` and a route-level use of it: a copy whose `fields` list has any row that is not an object with a text `field_id` is passed to the unchanged core as `{}`, which answers the existing `Invalid`. Any other exception reaches the shared `_forms` handler (logged error, controlled 503). The core is unchanged.
* `src/api/tests/test_form_held_download_api.py`: added `test_internal_type_error_is_a_logged_503_never_an_invalid_copy` (patches `draft_export` to raise `TypeError`) and `test_malformed_field_ids_are_invalid_for_any_binding_and_write_nothing` (integer and mixed ids against the own, another-case and missing-draft paths, no field details, state unchanged). The existing forged-copy control is unchanged and passes.
* `src/api/README.md`: replaced the unusable-copy sentence; states the Invalid-before-binding order and the 503 behaviour with the frozen-core limit.
* Amendment 2255 plan Phase 4 marker ticked with an annotation (assessment L3).

## Failing-first evidence

Before the route change (head `bad131ff2` plus the new tests only), the three targeted tests ran 3 tests with 6 failures: the internal `TypeError` answered 200 `Invalid` instead of 503, and the malformed ids answered `Unavailable` or a non-`Invalid` result. Log: session files `m1-failing-first-2312.log`. After the change all 16 tests of the module pass.

## Divergences and limits

* Critique CR-1 accepted: a malformed copy is now `Invalid` before the case and draft are looked up, where a mixed-id copy aimed at a missing or other-case draft used to answer `Unavailable`. This discloses less and is documented. The 400 draft mismatch, 401, 403 and switch 404 precedence is unchanged.
* Critique CR-2 accepted: the frozen core still turns its own digest and row-parsing `TypeError` into `Invalid`; only faults escaping the core (for example in `draft_export`) now reach the 503. No core change is made.
* Original self-review ordering defect, the assessment `Revise` verdict, M1 and the L1, L2 and L4 findings are preserved. L1 test expansion is not done (no general L1 test sprawl).

## Validation (isolated venv, pip only, `python -s`, no uv, no source-package `PYTHONPATH`)

Venv under the session files folder, installed with the hashed `src/api/requirements.txt` and `pip install -e ../core -e ../agents -e ".[dev]"` as the CI job does, `ruff==0.17.1`, `mypy==2.4.0`. Test-helper `PYTHONPATH` only (`../core/tests:../agents/tests`).

* `ruff check .`: All checks passed. `ruff format --check .`: 152 files already formatted. `mypy`: Success, no issues in 236 source files (from `src/api`, final tree).
* An earlier run before the CI-style dev install reported 64 mypy errors, 61 of them `playwright` import-not-found and 3 existing unrelated, none in the changed files; it is superseded by the dev-install run and kept in the log history only as an environment note.
* API `test_form_held_download_api` 16, `test_form_staging_api` 14, `test_role_endpoint_inventory` 24, `test_keepalive` 4; core `test_form_export` 11, `test_form_dependencies` 10: all OK. `git diff --check` clean.
* Not run: SQL Server, browser, axe, hosted CI, complete or `--changed` gate, cloud or model calls. Hosted CI on the exact head is unobserved; the head is unpushed.
