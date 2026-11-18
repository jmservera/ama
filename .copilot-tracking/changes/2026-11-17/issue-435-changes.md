---
title: Issue 435 changes
ms.date: 2026-11-17
---

Refs #435. Focused tier (documentation plus one tools unit test); no SQL, security, infrastructure or deployment scope.

## Changes

* docs/capstone/pitch/tokenomics-placement-draft.md: status table criteria 3, 5, 6 and status paragraph reconciled with delivered artifacts; criterion 3 kept Open because the rehearsal record is blank; ms.date 2026-11-17.
* tools/test_capstone_pitch_docs.py: new test (relative links resolve; draft statuses match delivered artifacts and the blank rehearsal record).

## Measurement and validation

* Before fix: new test failed on criterion 5 row ("Unmet. No revised deck exists"), reproducing the stale status.
* After fix: `python3 -m unittest tools.test_capstone_pitch_docs` OK (2 tests).
* `ruff format --isolated --line-length 100 --check tools/test_capstone_pitch_docs.py`: already formatted.
* `python3 tools/check-legacy-references.py`: 11 violations, identical failure at base (pre-existing, unrelated).
* mypy and src tests: not applicable (no src change). rpi-checks --all not run (heavy lock; focused tier).

## Not changed

No deck, price, placement, issue text, spend or rehearsal record. Unmet or unproven: criteria 1 (no deck rebuild), 2 (no mentor confirmation), 3 (no performed rehearsal; the issue tick conflicts with the blank record, needs human reconciliation), 4 (no live batch run).
