---
title: Issue 96 diagnostic D1 plan
description: Plan for the bounded Held download test-harness typing correction
ms.date: 2026-11-10
---

## Scope

One validation-harness correction for the Held download consumer (Refs #96). Research: `.copilot-tracking/research/2026-11-10/issue-96-diagnostic-d1-1110-research.md`. No production, core, guard, rights or browser-assert change.

## Phases

* [x] Phase 1: extract `FormApiFixture` (setUp, shutdown, call, working_review) in `src/api/tests/test_form_staging_api.py`; `FormApi` inherits it unchanged otherwise.
* [x] Phase 2: `src/api/tests/test_form_held_download_api.py` uses `import test_form_staging_api as staging`, subclasses `staging.FormApiFixture`, and replaces the two direct `server.held_download_enabled` asserts with real-route trusted-proxy checks.
* [x] Phase 3: default configured API `mypy` (no selectors) exit 0 with pinned 2.4.0; ruff 0.17.1 check and format on changed and new files.
* [x] Phase 4: affected unit modules and the served Held-download browser checker under the non-queued heavy lock.
* [x] Phase 5: additive qualification record of the earlier mypy claim, changes record, review, local commit, handoff.

## Gates

* Test counts must be unchanged for `test_form_staging_api` (14); the new module keeps 5 tests.
* Stop if a fix needs production, core, schema or refactor changes.
