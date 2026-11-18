---
title: Issue 521 live changes
description: Changes record with per-criterion proven/unproven table
ms.date: 2026-11-18
---

Tier: FOCUSED (documentation and evidence only; no `src/` change; `rpi-checks.py --all` not run). Refs #521.

## Changes

* Added `docs/reference/research/resident-demo-authority-live-521-2026-11-18.md`, index row in `docs/reference/README.md`, log entry in `docs/reference/log.md`.
* Added evidence `.copilot-tracking/evidence/2026-11-18-issue-521-live/` (script, JSON, two screenshots).
* No Azure mutation; no resource created.

## Validation

* `src/core`: `python3 -m unittest tests.test_resident_showcase tests.test_resident_showcase_sql` with `PYTHONPATH=src:tests`: 82 OK, 27 skipped.
* `infra`: `python3 -m unittest tests.test_resident_demo_secrets tests.test_resident_demo_deploy`: 33 OK.
* Live: `az containerapp show` reads and a Playwright desktop sign-in (see note). Credentials not printed.
* mypy and ruff: not applicable, no Python source changed (the evidence script is under `.copilot-tracking/`).

## Per-criterion table

| Criterion | Status | Basis |
|-----------|--------|-------|
| 1 Authority end consistent in code, SQL, helper, docs, tests (ticked) | Proven for source | Constant 2028-01-01 and focused tests pass |
| 2 Cost estimate and cap, nothing added (ticked) | Not re-proven here | Prior record; no resource added in this run |
| 3 Rotation steps documented (ticked) | Not re-proven here | No rotation per owner decision |
| 4 Live Azure change applied, verified, recorded | Partly proven | Live app expiry 2028-01-01T00:00:00Z and live sign-in proven. Live SQL window/constraint and image source commit unproven (private network) |
