---
title: Issue 96 diagnostic D1 details
description: Phase details for the bounded test-harness typing correction
ms.date: 2026-11-10
---

## Phase 1

* In `test_form_staging_api.py` add `class FormApiFixture(unittest.TestCase)` holding `setUp`, `shutdown`, `call` and `working_review` moved verbatim; `class FormApi(FormApiFixture)` keeps all `test_*` and other helpers. No body change.
* Check: `test_form_staging_api` still runs 14 tests (the fixture class has none).

## Phase 2

* Import line to the repository convention (plain sibling import).
* `class HeldDownload(staging.FormApiFixture)`; drop the four class-attribute borrows.
* Trusted-proxy: in the default-OFF test patch `self.app.provider.name` to `trusted-proxy` with the ON env and assert 404, no attachment, and the review view lacks `held_download_enabled`. If the provider name cannot be patched on the owned app instance, use `patch.object` on its class attribute within the test; stop if neither works without production change.
* Remove the unused `server` import if no longer used.

## Phase 3

* From `src/api` with the pinned venv: `python -m mypy --no-incremental --cache-dir <external>` with no file selectors; then `ruff check src tests checks`, `ruff format --check` on the changed and new files only.
* Pre-existing files unformatted under 0.17.1 are noted, not reformatted.

## Phase 4

* `unittest discover` for `test_form_held_download_api`, `test_form_staging_api`, `test_finance_grants_screens`, `test_role_endpoint_inventory`, `test_role_screens_conformance`; core export/dependencies/review/staging reruns.
* Browser checker via `flock -n /tmp/ama-rpi-heavy.lock`; busy means stop, no queue or bypass.

## Phase 5

* Additive record `issue-96-diagnostic-d1-1110-qualification` inside the changes record states that the parent "mypy pass" was file-selector only. Original artifacts untouched.
