---
title: Changes for #154 live round 4
ms.date: 2026-11-18
---

## Files

* New `src/api/src/zava_forward/api/resident_demo/rep_grants.py`; wired in `__main__.py` (`ZF_DEMO_REP_GRANTS_PATH`).
* New `src/api/tests/test_rep_grants.py` (4 tests); `src/api/README.md` setting note.
* New `docs/reference/research/issue-154-live-resident-ux-r4-2026-11-18.md`; index and log entries.
* The round-3 state file was replaced by this run's state (prior content stays in git history).

## Validation (tier: FULL applies to src changes; `rpi-checks.py --all` was not run per the brief, so no full receipt exists)

* `unittest tests.test_rep_grants tests.test_representative_expiry_api tests.test_resident_demo_api` from `src/api`: 57 tests, OK.
* `python3 -m mypy` in `src/api`: no issues in 349 files. `ruff check`: pass. `ruff format --isolated --line-length 100 --check`: pass.
* Web UI files, browser-check scripts, SQL, infra and workflows untouched; the accessibility, content-standard and manifest tests do not apply.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Journeys | Proven earlier (round 2) | Live captures |
| 2 Non-digital alternative and adjustments | Proven earlier (round 2) | Live captures |
| 3 Representative task-limited, expiring | Proven locally over HTTP; unproven live | New test; live needs redeploy plus grants file |
| 4 Offers vs commitments | Proven earlier (round 2) | Live captures |
| 5a No live resident contact | Proven for demo (round 3) | Network trace, Azure check |
| 5b Usability programme validation | Unproven, not demo scope | Needs moderated sessions |
