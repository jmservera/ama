---
title: Issue 74 Criterion 2 changes
ms.date: 2026-11-14
---

## Files changed

* `src/api/tests/test_home_case_api.py`: two tests.
  * `test_payload_keeps_building_and_home_records_in_separate_regions` seeds a dependency and a hold, then for ZF-2 and ZF-3 asserts the `building` payload has no home keys and the `home` payload has no building keys; building tokens (DEP-1, HOLD-1, WORK-1, COST-1, 12000.00) are absent from the home payload; home documents, measures and 6000.00 are absent from the building payload; the sibling's evidence is absent from the other home; the building payload is identical for both homes.
  * `test_screen_source_renders_each_record_type_in_one_region_only` slices `homeCaseView` by the `hc-home`, `hc-building` and `hc-versions` sections and asserts each record type is rendered in exactly one region.
* `src/api/checks/home_case_browser_check.py`: `check_regions_apart` run for ZF-2 and ZF-3 asserting two-way token absence, sub-headings (Evidence documents, Quality outcomes, Cost allocation versus Shared systems, Dependencies, Work stopped pending review, Shared works), and that the regions neither nest nor overlap.

## Manifest invariant

`scenario-manifest.json` and `scenario_manifest.py` do not reference `home_case_browser_check.py` (grep count 0 in each); no recipe SHA update was needed. `test_scenario_manifest.py` and `test_needs_inventory.py` pass.

## Canonical lock run

* Lock path: `/tmp/ama-rpi-heavy.lock` (`HEAVY_LOCK_PATH` in `tools/rpi-checks.py`).
* Mechanism: `flock -xn` (`LOCK_EX | LOCK_NB`, not queued) wrapping the command; free before the run.
* Holder verification: inside the held lock, a second non-blocking acquire was refused (`second-acquire-refused`); holder pid recorded in the run output.
* Command (cwd `src/api`, worktree `PYTHONPATH`, `ZF_AXE_JS` pinned axe 4.10.3, sha256 880970c0...a68bb verified by the check): `python3 -m checks.home_case_browser_check`.
* Final run 2026-11-14T08:46:42Z to 08:46:46Z on the committed file content: exit 0, 34 PASS lines, `COMPLETE: all checks ran, including axe 4.10.3`, no writes, no JavaScript errors.

## Validation

* `python3 -m unittest` for the four named modules (explicit worktree `PYTHONPATH`): 30 tests OK.
* `ruff check` and `ruff format --check`: clean (one format fix applied).
* `mypy` on `home_case_browser_check.py`: clean when run from `src/api` (canonical cwd). Run from the repository root it reports two import-resolution errors that are identical on unmodified `main` (pre-existing, environmental).
* Hosted CI: not observed (nothing pushed).
