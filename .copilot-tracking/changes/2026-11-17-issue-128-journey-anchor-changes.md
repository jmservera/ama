---
title: Issue 128 changes
ms.date: 2026-11-17
---

## Planned

* `src/core/src/zava_forward/core/journey_register.py`: resolvable `design_ref` anchors.
* `src/core/tests/test_journey_register.py`: anchor regression test.
* `docs/reference/research/ux/equity-journey-test-plan.md`, `docs/reference/log.md`: record the fix.

## Baseline

Measured on main: 0 of 7 `design_ref` anchors resolve to a heading in `residents.md`.

## Done

* `journey_register.py`: added `_anchor`, `design_ref` now the heading slug. Test added. Test plan and log updated.
* Pre-fix evidence: the new test failed (`'j1' not found` among document slugs) against the unmodified module.
* Validation (from `src/core`, `PYTHONPATH=$PWD/src` because the editable install points at the main checkout): `python3 -m unittest tests.test_journey_register tests.test_usability_programme tests.test_paired_equity tests.test_resident_journey_design -q` 62 OK; `ruff check .` pass; `ruff format --check .` 274 formatted; `mypy` no issues in 327 files.
* Not run: full gate (lock held), api suite (no api change), browser checks (no web change). Web guidance not applicable (no web edit).
