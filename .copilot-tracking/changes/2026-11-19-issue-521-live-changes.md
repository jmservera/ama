---
title: Changes for issue 521 live run (2026-11-19)
description: Evidence-only changes and per-criterion table
---

## Changes

* Added [run 3 research note](../../docs/reference/research/resident-demo-authority-live-521-r3-2026-11-19.md), index row and log entry.
* Added evidence in `.copilot-tracking/evidence/2026-11-19-issue-521-live/`.
* No `src/`, `infra/` or Azure change; no throwaway resource created. Divergence: none.

## Validation (FOCUSED, no src change)

* `src/core`: `unittest tests.test_resident_showcase tests.test_resident_showcase_sql`: 82 tests OK, 27 skipped (SQL-dependent).
* `infra`: `unittest tests.test_resident_demo_secrets`: 16 tests OK.
* mypy and ruff not applicable: no Python source changed. Web checks not applicable. `rpi-checks.py --all` not run.
* Hosted CI, human approval and independent exact-head review not observed.

## Per-criterion table

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 1 Authority end consistent across code, SQL, helper, docs, tests | Proven (source) | core-tests.txt, infra-tests.txt |
| 2 Cost estimate and cap, nothing added | Proven by prior record; nothing added this run | run 1 note, USD 440.90 of 700 |
| 3 Rotation and renewal documented | Proven by prior record; no rotation per owner | infra README |
| 4 Live change applied after owner confirmation, verified, recorded | Partly proven | App expiry `2028-01-01T00:00:00Z` and HTTPS sign-in proven (az-resident-demo.json, live-checks.json, screenshots). Unproven: live SQL window (private-only), apply timestamp, image-to-commit |
