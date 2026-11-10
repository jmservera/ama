---
title: Issue 1384 workspace exhaustion oracles plan
description: Plan to derive the two workspace exhaustion expectations from the declared script-retry contract with controlled negative controls
ms.date: 2026-11-10
ms.topic: reference
---

## Task

* Task: `workspace-oracles-1384-1110`; issue #1384; branch `fix/demo-workspace-retry-oracles-1384-1110`; pinned main `caaf989148aff21ed8ecb5b71eb0be75b29c16de`; target main.
* Research: `.copilot-tracking/research/2026-11-10-workspace-oracles-1384-1110-research.md` (disposition executed, Planning Readiness Ready).
* Details: `.copilot-tracking/details/2026-11-10-workspace-oracles-1384-1110-details.md`.
* Tier: demo focused. Checker-only; production `app.js`, loader, delays, auth, API, aftercare, service, store and operational policy stay unchanged.

## Objective

Make the two exhaustion oracles correct for the existing contract (one load plus one request per declared `SCRIPT_RETRY_DELAYS` entry, stopping on any non-error outcome), derived from the declaration with a loud failure when it is absent or malformed, and prove with controlled changed loaders that extra attempts, early termination, a route-revisit budget reset and a missing-global continuation are detected.

## Phases

* [ ] Phase 1: shared helper `src/api/checks/script_retry.py` (strict declaration parser, derived totals, controlled `app.js` transformations, route helper).
* [ ] Phase 2: `workspace_scripts_browser_check.py` exhaustion oracle and controls (extra, early, reset on the repeated-abort branch; continue on the missing-global branch).
* [ ] Phase 3: `employee_workspace_browser_check.py` missing-ops oracle and controls (extra, early).
* [ ] Phase 4: coupled regression tests in `src/api/tests/test_workspace_scripts.py` (strict parser, helper totals equal the real loader in a Node VM, each controlled transformation really changes the loader).
* [ ] Phase 5: focused validation (loader tests, both actual served browser checks, ruff, mypy, `node --check`), changes record, review.

## Decisions

* Expected exhaustion total is `1 + len(delays)` from the strict parse of `app.js`; the missing-global total stays the separately proved literal `2` (initial plus the single retry that stops after a successful evaluation without the global). No total comes from observed requests and none is a blind 3 to 4.
* Negative controls transform only the served `app.js` text inside the check (route fulfilment), never the repository file. Each transformation must match exactly once or the check fails loudly.
* The lenient parser in `loading_briefing_browser_check.py` is not touched (outside the two-checker grant); routed as follow-up.
* Failures use distinct assertion messages so a control can require the intended assertion rather than any `AssertionError`.

## Validation (focused tier)

* `python -m unittest tests.test_workspace_scripts` and the other existing loader/check tests that import `checks.*` for the touched modules.
* Both actual served checks under non-queued `flock -n /tmp/ama-rpi-heavy.lock`; non-heavy checks first; one later browser attempt if the holder is busy, else held output.
* From `src/api`: `ruff check`, `ruff format --check` (per configuration), `mypy`, and `node --check` on `app.js` (unchanged).
* Not run: full gate, `--changed`, SQL, images, cloud, accessibility acceptance.

## Risks

* Route fulfilment with a transformed `app.js` could be invalidated by a future `app.js` shape change; mitigated by the exactly-once match and by unit tests that drive the same transformation through the real loader.
* Browser time grows by about five seconds per control (six controls total).
