---
title: Issue 162 live audit changes
ms.date: 2026-11-18
---

## Changes

* Added docs/reference/research/issue-162-live-audit-2026-11-18.md and folder issue-162-live-audit-2026-11-18/ (scripts and raw output; screenshots removed because the workbench shows case names).
* Updated docs/reference/README.md (one index row) and docs/reference/log.md (one entry).
* No src change. Tier FOCUSED (documentation and evidence). rpi-checks.py not run.

## Validation

* `python3 -m unittest tests.test_chat_isolation` in src/api: 33 tests OK.
* Live probe: 3 refusals audited, chain intact (2068 to 2070). Link check of the new note below.

## Per-criterion table (issue #162)

| Criterion | Status |
| --- | --- |
| 1. Queries keyed by authenticated user | Proven (live and local) |
| 2. Role matrix every endpoint, denies cross-user | Proven locally; live foreign-thread read unproven (one Entra identity) |
| 3. Same field-level projection | Proven locally; not live |
| 4. Never shared into another user's prompt | Proven locally; not live |
| 5. Prompt injection cannot cause tool calls, exposure or writes | Proven locally; not re-run live |
| 6. Admin and break-glass audited with purpose, policy decided | Partly proven: refusals live, grants local only, policy demo-only. Leave unticked |

Production-only: DPO and Legal approval, administrator Entra role, user notification, audit retention, content access, real two-user test.

## Deviation

The brief's state-file path collided with the tracked record of an earlier run. That record is restored unchanged; this run's state is in `issue-162-live-r3-state.json`.
