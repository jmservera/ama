---
title: Issue 119 changes
description: Change record
ms.date: 2026-11-17
---

## Planned changes

* Add docs/design/map-tile-provider-decision-record.md
* Edit docs/reference/research/ux/map-tile-provider-options.md (link), docs/reference/README.md, docs/reference/log.md
* Add src/api/tests/test_map_tile_decision_record_119.py

## Validation

Recorded below after implementation.

## Implemented

Created decision record, test file; edited options doc, README index, log.

## Validation (FOCUSED; 2026-11-17)

* Red first: new test failed on missing options-doc link and a brittle assertion (corrected).
* `cd src/api; PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p <module>`: test_map_tile_decision_record_119 (5 OK), test_epic149_ux_journey_requirement_traceability (10 OK), test_ui_support (12 OK).
* `ruff format --isolated --line-length 100 --check` on the new test: already formatted. `mypy` on the new test: no issues.
* Not run: rpi-checks --all, browser/screen reader (not touched; heavy lock held by another gate), src/core suite (no core change).
* Tier basis: docs plus one unit test; no SQL, security, infra or deployment change.
