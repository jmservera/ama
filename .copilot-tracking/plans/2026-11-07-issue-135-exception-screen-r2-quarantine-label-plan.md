---
title: Issue 135 exception screen r2 quarantine label correction plan
ms.date: 2026-11-07
---

* Research: `.copilot-tracking/research/2026-11-07-issue-135-exception-screen-r2-quarantine-label-research.md`. Details: `.copilot-tracking/details/2026-11-07-issue-135-exception-screen-r2-quarantine-label-details.md`.
* Tier: focused. Scope: `role-screens.js` (`exceptionHappened`) and `test_exception_register_screen.py` only.

## Phases

* [x] Phase 1: update the test fixtures to the real returned values and add a reason-less item; run against the OLD renderer and record that it fails.
* [x] Phase 2: change `exceptionHappened` to the case-insensitive quarantine test and the reason-gated fallback wording.
* [x] Phase 3: rerun the focused unit tests, ruff, format, mypy and `node --check`.
* [x] Phase 4: refresh the web guidelines, changes record and one r2 Review; commit.
* [ ] Phase 5 (after freeze): `rpi-checks --changed` focused gate and the external real-DOM story on a new git-archive export.

## Critique (one pass, final candidate)

Executed 2026-11-07 against this plan before any code change. Verdict: proceed with direct amendments.

* Finding 1 (applied): lowercasing alone would still call a reason-less, non-quarantined failed-AI item a fallback. Gate the fallback wording on a non-empty string reason and say how it failed is Unknown otherwise.
* Finding 2 (applied): the old fixtures (`"quarantined"`, `"fallback"`) were not real values and masked the bug. Use `"Quarantined"` and `"Not reviewed"`, and keep one lowercase case only as compatibility.
* Finding 3 (applied): the failed-before proof must run the new test against the unmodified renderer and be recorded before the fix.
* Finding 4 (recorded, not applied): validating every returned status string is out of scope. The unit fixture cannot replace the real-DOM story, which stays a separate required check.
