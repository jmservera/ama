---
title: Issue 76 changes
ms.date: 2026-11-19
---

Refs #76. No source change; tier FOCUSED. Validation: targeted tests below (9 tests OK, run on this head). mypy, ruff and web-baseline checks not applicable (no src or web edit).

| Criterion | Status | Evidence |
| --- | --- | --- |
| Default view single list, one status, one next action | Ticked | Already ticked in issue |
| No perspective picker | Ticked | Already ticked |
| Queue with visible definitions | Ticked | Already ticked |
| Blocked steps reason, owner, action | Ticked | Already ticked |
| Hazard and safeguarding show clock and named owner | Proven for safeguarding live (r4, revision 33); hazard clock and owner proven, time values Unknown (no awareness timestamp in synthetic record). Code and unit tests exist and pass. Left unticked: whether Unknown counts as a clock is an issue-owner call | [r4 note](../../docs/reference/research/issue-76-live-r4-2026-11-19.md), `src/api/tests/test_workbench_hazard_clock_owner.py` |
| Ownership agreement (FR-034) | Ticked | Already ticked |
| Single reset (FR-032) | Ticked | Already ticked |
