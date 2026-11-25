---
title: Changes issue 2303 r73
ms.date: 2026-11-25
---

## Changes

* `src/core/src/zava_forward/core/ai_tasks.py`: `live_report` computes `withheld_scope_values` once per distinct ordered case set per call.
* `src/core/tests/test_live_report_withheld_scan.py`: new test; passes with the fix and fails (`4 != 2`) on the old code.
* Validation: 607 related core tests OK (skipped 164, pre-existing skips); mypy leaves only the 3 pre-existing errors (telemetry x2, device_provision); ruff check passes; ruff format applied to the new test.
* Evidence: `docs/reference/research/issue-2303-live-2026-11-25-r73.md` with `live-r0000073.json`, `.png` and the probe script; index and log updated.
* Tier: FULL (src change). The full gate and external receipt were not run by this worker (forbidden); the coordinator owns them.
* Not done: no image build or deployment, so live latency after the fix is unmeasured.

## Per-criterion table

| Criterion | Result | Evidence |
| --- | --- | --- |
| 1 Local regression test fails without the golden file or variable | Proven | `test_image_chat_golden_contract.py` and core `test_cutover_audit` (see r72 note) |
| 2 Dockerfile copies chat_golden.json and sets ZF_CHAT_GOLDEN | Proven | `src/api/Dockerfile` copy and `ZF_CHAT_GOLDEN` setting; unchanged |
| 3 After deployment GET /api/ai/report returns 200 and Asset and board view loads | Proven on 0000073 (latency caveat) | 200 on four calls (86.9, 79.4, 69.6 s API; 70.3 s UI); latency remains a defect, fixed in source only |
| 4 Full tier: complete local gate and external receipt | Unproven | `rpi-checks.py --all` forbidden to the worker; coordinator runs the gate; the src change makes the full tier applicable |
| Follow-up: report answers fast on the demo | Unproven | cache did not help (cost is in `live_report`); memo fix awaits deployment and re-probe |
