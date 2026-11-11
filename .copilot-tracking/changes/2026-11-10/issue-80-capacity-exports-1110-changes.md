---
title: Issue 80 capacity page export controls, changes
description: Prospective and actual changes record for the two Capacity page CSV anchors
ms.date: 2026-11-10
---

## Prospective changes (written before implement-start)

* `src/api/src/zava_forward/api/web/ops.js`: one local helper and two conditional anchors in `capacityView`.
* `src/api/checks/capacity_browser_check.py`: focused assertions for both anchors (seeded download and empty withheld).
* No other source, test, config, dependency, workflow, KB, index or log change. Old RPI records and evidence are untouched.

## Actual changes

* `src/api/src/zava_forward/api/web/ops.js` (6 insertions, 1 deletion): local `exportLink` helper (line 485) and two conditional anchors (lines 490 and 494) with fixed hrefs `/api/packages.csv` and `/api/workorders.csv`, `class="btn alt"`, `download` filenames, visible labels "Download all packages for Excel" and "Download all work orders for Excel", and the sentence "The file has every package|work order you can see, not only the ones on this page. It is a read-only copy; changes in it are not imported back." Shown only when the response `total` is non-zero.
* `src/api/checks/capacity_browser_check.py` (+45): `import csv`; `export_download` helper (line 461) run for both anchors in the seeded scenario (one link, label, breadth and read-only text, keyboard Enter download, filename, CSV rows equal the unpaged JSON count, seeded id present, URL unchanged, no POST); and an `empty capacity` assertion of zero `a[download$='.csv']`. The file was `ruff format`ed; only my hunks changed (diffstat 45 lines).
* No other file changed. No dependency installed.

## Validation executed (focused tier) and outcomes

| Check | Command (cwd `src/api`) | Exit | Result |
| --- | --- | --- | --- |
| Node syntax | `node --check .../ops.js` | 0 | Pass |
| Style | `ruff check` and `ruff format --check` on the changed check (ruff 0.17.3, installed) | 0, 0 after one `ruff format` of my hunks (first format check exited 1 on my own long lines) | Pass |
| API unit tests | `python -m unittest tests.test_list_export_api -q` (owned venv, `PYTHONPATH` pattern) | 0 | 11 tests OK |
| Browser | `python -m checks.capacity_browser_check --axe /tmp/axepk/package/axe.min.js` once (the check takes `/tmp/ama-rpi-heavy.lock` itself with `LOCK_NB`; lock was free; not wrapped in another flock) | 1 | PARTIAL, see below |

Browser run 1 raw log: `ROOT/phase80-capacity-exports-evidence-1110/browser-run1.log`, exit `browser-run1.exit`.

* Executed and passed before the failure: seeded capacity render (1 package, 20 of 601 work orders on the first page); axe `seeded capacity` with 0 violations and 0 incomplete; `Capacity export packages.csv: PASS; 1 rows, keyboard Enter`; `Capacity export workorders.csv: PASS; 601 rows, keyboard Enter` (the unpaged CSV held all 601 rows while the page showed 20, so the "not only the ones on this page" label is accurate in this fixture); manager routes `#/` to `#/assistants` passed.
* FAILED: manager route `#/time` at `capacity_browser_check.py:395`, `AssertionError: Locator expected to have text 'Time capture is switched off.'` while the page showed "Time capture is switched off, so nothing can be recorded. Owner: application support. Next action: ...". Cause by source reading: the check compares the status text with the API `reason`, while `timecapture.js` (commit `a740072d1`, #1343) now renders reason plus owner and next action. This is an existing drift in an unrelated route that I did not touch and did not repair (not requested, and a re-run is not admitted). It is a source-read attribution, not a baseline re-run.
* NOT EXECUTED because the failure ended the single run first: the `empty capacity` scenario, including my new zero-anchor assertion, and the later failure/retry scenarios. The withhold-on-empty behaviour is therefore verified by source reading only (`total ? link : null`), not by a runtime result.
* The overall browser check did not pass. This is not a whole-check pass and must not be reported as one.
* Owned data: the check writes a synthetic seed under `/tmp/ama-capacity523-*` (removed on exit; none remained), uses an in-process loopback ephemeral server and a scrubbed environment (`PATH HOME TMPDIR LANG LD_LIBRARY_PATH`). Default `~/.zava-forward` data was never opened. No helper process remained.
* Skipped, not run: full gate, `rpi-checks`, mypy, hosted CI, screen reader, rendered layout beyond Chromium DOM, any SQL/Docker/Azure/provider activity.
