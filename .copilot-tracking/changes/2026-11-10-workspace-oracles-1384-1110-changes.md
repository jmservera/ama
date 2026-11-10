---
title: Issue 1384 workspace exhaustion oracles changes
description: Changes record for the two workspace exhaustion oracles, prospective until implementation finishes
ms.date: 2026-11-10
ms.topic: reference
---

## Status

* Implementation complete for the checker-only change; one open finding is held (see Held Finding). Plan: `.copilot-tracking/details/2026-11-10-workspace-oracles-1384-1110-details.md`.
* Base: commit `477d7b7a91639e072ab17d0fbad8142e8b3cb4fe` on pinned main `caaf989148aff21ed8ecb5b71eb0be75b29c16de`.
* No production file changed (`app.js`, loader, delays, auth, API, aftercare, service, store, policy are untouched).

## Files Changed

* `src/api/checks/script_retry.py` (new): strict parser of the `SCRIPT_RETRY_DELAYS` declaration (loud `ValueError` when missing, duplicated or malformed), `exhausted_requests()` = 1 + number of delays, `MISSING_GLOBAL_REQUESTS = 2`, four controlled `app.js` transformations (`extra`, `early`, `reset`, `continue`), `serve_mutated_app`, exact `assert_requests` and `expect_detected`.
* `src/api/checks/workspace_scripts_browser_check.py`: `exhaustion()` derives its count from the helper and gains an optional mutation; new `exhaustion_controls` runs four negative controls.
* `src/api/checks/employee_workspace_browser_check.py`: `original_ops == 3` replaced by the derived exact oracle; new `missing_ops_controls` (extra, early).
* `src/api/tests/test_workspace_scripts.py`: new `ScriptRetryOracle` tests (parser negatives, derived totals equal the real loader in a Node VM, each mutation diverges as expected, unsafe transformations refused, exact-failure matching). Existing tests unchanged.

## Validation (focused tier, from `src/api`, own venv `/home/azureuser/.cache/ama-venv-1384-workspace-oracles-1110`)

* `unittest tests.test_workspace_scripts`: 10 OK.
* `ruff check .`: pass. `ruff format --check .`: pass. `mypy` (strict): no issues in 216 files. `node --check app.js`: pass.
* `employee_workspace_browser_check.py`: exit 0, including the original `missing_ops_recovery` and the extra/early controls (expected 4, observed 5 and 3). Raw: evidence `04-after-employee_workspace.*`.
* `workspace_scripts_browser_check.py`: exit 1. The exhaustion oracle, the missing-global branch and all four controls now PASS (extra 4/5, early 4/3, reset 4/7, continue 2/4). The run then fails later at `assert len(pending) == 1` in `delayed_companion` (line 274). Raw: `04-after-workspace_scripts.*` (fails in the sign-out variant) and the single permitted rerun `05-rerun-workspace_scripts.*` (fails in the timed-out variant).

## Held Finding

* `delayed_companion` has a separate pre-existing race: the script element appears before the intercepted request is recorded in `pending`. A probe of the unmodified original function (evidence `06-baseline-delayed-companion-probe.*`, 16 calls) failed once (sign-out variant). It is not the exhaustion oracle and is not changed here (owner scope). The scripts check is therefore not observed green; this is held as a distinct finding.

## Deviations and Disclosures

* A foreign lock holder existed at the first probe and was gone before the first run; no queueing, spinning or killing.
* A few earlier evidence and document edits were made by small Python scripts rather than the edit tool; later source edits used the edit tool except two one-line `sed` test tweaks.
* Temporary probe files under `src/api/checks/` were removed.
