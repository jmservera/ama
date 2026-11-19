---
title: Issue 462 live r4 changes
ms.date: 2026-11-19
---

Refs #462. Session `rpi-462-live`, task `issue-462-live-r4`.

## Changes

* `src/core/src/zava_forward/core/resident_preview.py`: `safe_start` now requires the dataset `fixture_id` (and, by equality, the fixture `id`) to be a non-blank string. Closes the High review finding `discussion_r4372517587` on PR #455: two missing or null ids previously compared equal and were accepted.
* `src/core/tests/test_resident_preview.py`: `test_refuses_missing_null_or_blank_fixture_identifiers` covers missing, null-equivalent, empty, blank and numeric ids, on both sides together and on the marker alone. Without the source fix 5 subtests fail; with it all pass.

## Validation (FOCUSED local; src change classifies FULL, `rpi-checks.py --all` not run per owner brief)

| Command | Result |
|---------|--------|
| `src/core`: `python3 -m unittest tests.test_resident_preview` | 37 tests OK (5 failures with the fix reverted) |
| `src/api`: `tests.test_resident_preview_api tests.test_resident_demo_api` | 66 tests OK |
| `src/core`: `python3 -m ruff check` and `ruff format --isolated --line-length 100 --check` on both files | pass |
| `src/core`: `python3 -m mypy` | 22 errors, all in `telemetry.py` and telemetry tests (missing `opentelemetry` stub in this environment); none in the changed files |
| `src/core`: `tests.test_resident_preview tests.test_resident_showcase tests.test_profile_journey_contract` | 87 tests OK |
| `src/core`: full `unittest discover` | started, stopped after over 20 minutes without result; not claimed |

## Per-criterion table

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven (earlier runs) | r3 note; this run's artifacts |
| 2. #444/#455 and failed rubric resolved | Partly proven, still unmet | Closed/merged and scorer success at the final head (r3 note). The unresolved High finding is now fixed in main-derived code by this commit. Not provable locally: absence of manual score edits, a hosted rerun (scorer `disabled_manually`; no push allowed), and resolution of the GitHub thread itself |
| 3, 4, 5, 8 (ticked) | Not re-run | No change to their scope |
| 6. Pre-spend record | Proven for the demo (r3 note) | Owner decision supersedes the October cap; cost refresh was throttled |
| 7. Deployed showcase in a browser | Proven for the demo, desktop (r3 note) | Not repeated; no source change to deployed code, and this change affects only the loopback preview start-up |
