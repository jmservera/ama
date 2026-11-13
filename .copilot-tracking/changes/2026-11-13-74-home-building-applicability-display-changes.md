---
title: Changes for #74 home view building applicability display
ms.date: 2026-11-13
---

Base `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626`; topic `feat/demo-home-applicability-74-0458`. Refs #74 (no closing keyword; no AC tick).

## Critique (one pass, independent)

Agent: rubber-duck subagent (separate context, read-only). Verdict: Proceed with changes.

* C1 (blocking): static string asserts duplicate `buildingView`; require executable row-level tests for null, empty, multiple and absent scope, failing before the change. Applied: the browser check seeds WORK-U, WORK-N and WORK-M and asserts rendered text; run red against base `app.js`, green with the change.
* C2: the display could imply a home-package determination. Applied: label "Recorded scope" and add a note that scopes do not establish eligibility, approval or coverage.
* Write surface confirmed narrow; initial classification consistent with the supplied evidence (the historical correction count is not independently established); no new business meaning. No user decision required.

## Changes

* `src/api/src/zava_forward/api/web/app.js`: home-case `shared()` shows existing `case_ids` and `package_ids` as "Recorded scope. Homes: ... Packages: ..." (null = Unknown, [] = None, list = IDs; rows without scope fields, such as systems, unchanged) plus a non-eligibility note in the building region only.
* `src/api/checks/home_case_browser_check.py`: three synthetic works rows (unknown/none, none/unknown, multiple IDs) and assertions, including home-panel separation and no scope line on systems.
* `src/api/README.md`: one sentence on the check.

## Validation (focused; not a full gate)

* `node --check app.js`, ruff check, ruff format check and mypy on the changed check file: pass.
* `tests.test_home_case_api` (6 tests): OK, run with PYTHONPATH set to this worktree's `src/*/src` because the editable install resolves to another checkout (`/home/azureuser/source/ama`). An initial run against that install gave one unrelated 404 failure and an invalid red result; both were discarded.
* Browser: `python -m checks.home_case_browser_check` under `flock -n /tmp/ama-rpi-heavy.lock` (nonqueued, acquired; 4 CPUs, load below 1, about 4.8 GB available). Red against base `app.js` (new assertion failed); green with the change, all checks pass at 320 and 1280 px, read-only, no JS errors. Axe skipped (`ZF_AXE_JS` unset): no automated accessibility result.
* Web guidelines source fetched 2026-11-13 (rules and output format; tail not retrieved).
* No separate unit test was added; executable assertions live in the browser check, per critique C1.

## Not done

Full gate, hosted CI, SQL Server, human keyboard/screen-reader/WCAG acceptance, owner confirmation of the G5 display and the meaning of "outcome", independent exact-head assessment.
