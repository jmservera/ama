---
title: Issue 2303 live changes
ms.date: 2026-11-24
---

No `src/`, Dockerfile, workflow or dependency change. Tier: focused. Basis: documentation and a probe script only.

## Changes

* Added [issue-2303-live-2026-11-24.md](../../../docs/reference/research/issue-2303-live-2026-11-24.md) with probe script, JSON, screenshot and case-detail timing.
* Added an index line in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.
* Divergence from plan: none. Disclosure: one Playwright timeout message echoed a session cookie to the worker console during debugging; fixed in the probe, never stored.

## Validation

* `src/core` `tests.test_cutover_audit`: 10 tests OK.
* Live: nine 200s for GET /api/ai/report on revision 0000061; Asset and board view shows the report-present branch.
* Not run: `rpi-checks.py`, failing-mutation run of the regression test.

## Per-criterion table

| Criterion | Result |
| --- | --- |
| Local regression test fails when the image lacks the chat golden file or variable | Proven for the demo (test present, passing; failing mutation not observed) |
| Dockerfile copies `chat_golden.json` and sets `ZF_CHAT_GOLDEN` | Proven (Dockerfile lines 30 and 34) |
| After deployment GET /api/ai/report returns 200 and the Asset and board view shows a loaded report | Proven on 0000061, latency 66 to 186 s noted |
| Full tier gate and external receipt | Unproven: no source change, gate owned by the coordinator |
