---
title: Issue 432 changes
ms.date: 2026-11-17
---

## Planned changes

* `docs/reference/resources/ai-tokenomics.md`: current-main inventory section; supersede stale Gaps rows.
* `docs/reference/README.md`, `docs/reference/log.md`: index and log entry.
* `src/core/tests/test_ai_metering_inventory.py`: inventory drift and Unknown-cost regression test.

## Validation (to record)

Targeted unittest, `ruff format --isolated --line-length 100 --check`, mypy `src/core`. Not applicable:
rpi-checks --all (FOCUSED tier, heavy lock held), SQL, browser.

## Results (2026-11-17)

* Done: doc inventory section, README index row, log entry, `test_ai_metering_inventory.py` (4 tests).
* Divergence: the plan's second test case (Unknown cost without price) was dropped; it is already covered by
  `test_ai_consumption.py` (asserts `token_cost` Unknown, reconciliation `unreconciled`).
* Failing-first evidence: the first run of the new test failed (doc cited `complete` without the
  `Consumption.` prefix), proving it detects citation drift; fixed in the doc.
* Commands: `python3 -m unittest discover -s tests -p "test_ai_*.py" -q` in `src/core`: 92 tests OK;
  `ruff format --isolated --line-length 100 --check tests/test_ai_metering_inventory.py`: clean;
  `mypy .` in `src/core`: no issues in 328 files.
* Qualification: installed `zava_forward.core` resolves to the main checkout; `ai_consumption.py` unchanged
  between base and that checkout. Dotted `unittest tests.test_ai_consumption_safety` fails on `from dataset import`
  (path artefact); discover form passes.
* Not applicable: rpi-checks --all (FOCUSED, heavy lock held), SQL, browser, hosted CI not observed.
