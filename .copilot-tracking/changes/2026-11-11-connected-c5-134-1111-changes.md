# Changes: #134 connected same-home check (C5)

Date: 2026-11-11. Task: connected-c5-134-1111. Base: 35eb0e559c7d0660ab87594732675b71be7bee67 (origin/main unchanged when fetched before writes). Admission: [amendment](../plans/2026-11-11-connected-c5-134-1111-amendment.md), commit a837f28.

## Files changed

* NEW `src/api/checks/connected_home_browser_check.py`: pure helpers (`journey_snapshot` line 99, `snapshot_failures` 135, `leak_markers` 188, `home_expectations` 217, `sibling_expectations` 317, `expect_failures` 337, `home_failures` 378, `sibling_failures` 382) plus the keyboard walk (`walk_visit` 542) and `run_browser` 613.
* NEW `src/api/tests/test_connected_home_check.py`: six pure regressions.
* `src/api/README.md`: one paragraph after the home-case check paragraph.

No product, API, Store, role, manifest, workflow, prior probe, fixture-module or register file changed.

## Behavior

* The data served is `copy.deepcopy(store.data)` taken from the delivered `StoreJourney` helper before its cleanup. No journey step is re-implemented.
* Six screens read one fixture state through five constructed logins: Asset (via the Programme Manager, a proxy), Programme (menu carry with no reset), Technical, Resident choice, Quality, Finance.
* Every required marker is derived from the Store record and matched inside its named panel (row cells, field label and value, or panel text). A missing marker fails the run; nothing is reported as a gap and passed.
* Sibling ZF-2 is the negative control. Its own retained measure and stage must render ("Home scope: ZF-2 only", "Loft insulation: no quality check recorded", "No design is recorded for this home", "No invoices recorded for this home"), and distinctive ZF-1 values (query and source ids, names, scope, INV-100, the Handed over panel title, Cavity wall) must not appear in the scoped panels. Values that also occur in ZF-2 data are dropped as generic.
* Interpretation to confirm: A4 asked for distinguishable retained sibling data. ZF-2 has no journey records, so its distinguishing data is its own measure, stage and the screens' own no-record states, not a second completed journey.
* Run-only mutations (marker removed, heading, handoff link, menu link without the home; sibling leak and removed sibling panel) are judged by the same production predicates (`home_failures`, `sibling_failures`).
* The browser sends no non-GET/HEAD/OPTIONS request after login and raises no page error.

## Validation (private HOME, TMPDIR and cache under /tmp/z134)

| Command | Result |
| --- | --- |
| Missing import probe with system python (zava_forward, playwright, ruff, mypy) | failed, recorded; private venv then built with `pip install -e ../core -e ../agents -e ".[dev]"` (core, agents, api only) |
| `python -m unittest test_journey_store test_journey_trace -q` from `src/core/tests` (once, before writes) | 15 tests, OK |
| `python -m unittest tests.test_connected_home_check -q` from `src/api` | 6 tests, OK (also after the final edits) |
| `ruff check .` and `ruff format --check .` from `src/api` | pass, 150 files formatted |
| `mypy` (full API config, 234 files) | no issues. First run found strict-typing errors from following the core test module; fixed by importing it by name |
| `flock -n -E99 /tmp/ama-rpi-heavy.lock timeout 900 python -m checks.connected_home_browser_check` (one run) | exit 0, 120 PASS lines, 6 negative controls rejected, no failure, log `/tmp/z134/browser.log` |

Chromium 1248 from the existing Playwright cache with Playwright 1.64.0 launched. Axe was not run (not in S1). No skips. No browser rerun was needed.

## Limits

Not run and not claimed: perspective rows 6, 7, 8 and 11, entry by report or nomination, intake and aftercare, event order, eight-stage consistency, a real Asset sign-in, AC-034 to AC-043, assistive technology, user validation, consent and human approval. Sibling mutations ran on the Asset screen only; other sibling screens are checked by the pure tests and the single browser pass. The 14th specialist screen drift in the keyboard probe is separately owned and untouched. No criterion is ticked.
