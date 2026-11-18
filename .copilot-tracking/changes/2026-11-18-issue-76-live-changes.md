---
title: Changes for issue 76 live proof
ms.date: 2026-11-18
---

Refs #76. Tier FOCUSED; no `src/` change, so FULL tier does not apply. `rpi-checks.py --all` was not run. Note: the docs and evidence were drafted before the `implement-start` witness call (the changes file was written after the live run), disclosed here.

## Files

* `docs/reference/research/issue-76-live-task-queue-evidence-2026-11-18.md` (new), `docs/reference/README.md` (index line), `docs/reference/log.md` (entry).
* `.copilot-tracking/evidence/2026-11-18/issue-76-live/` scripts, JSON outputs, screenshots, failed first UI run kept.

## Per-criterion table

| Criterion | Proven live on demo | Notes |
| --- | --- | --- |
| Default view single list, one status, one next action | Already ticked; not re-opened | |
| No perspective picker or role simulator | Already ticked; not re-opened | |
| Queue with visible definitions | Already ticked; not re-opened | |
| Blocked steps reason, owner, next action | Already ticked; not re-opened | |
| Hazard and safeguarding show clock and named owner | Partly: hazard yes (named owner Karen Lawson, clock line shows "elapsed time unknown"); safeguarding unproven | No timestamps in demo record; no demo case has a safeguarding item; no data was created |
| Views agree (FR-034) | Already ticked; not re-opened | |
| Single reset to default (FR-032) | Already ticked; not re-opened | |

## Validation

* `src/api` unittest `test_workbench_hazard_clock_owner`, `test_safeguarding_clock_a11y`, `test_safeguarding_detail_boundary`: 9 OK. `src/core` `test_taskqueues`: 29 OK.
* mypy and ruff: not applicable (no Python changed). Web UI files unchanged, so the accessibility and content-standard tests were not required.
* Azure: read-only; no resources created, none to delete. Credential values never printed.
