---
title: Changes for issue 2245 (2026-11-24 live run)
ms.date: 2026-11-24
---

## Changes

Planned: `src/core/src/zava_forward/core/continuity.py` and `src/core/tests/test_demo_owner_override.py` (override keyed on the demo profile); research note `docs/reference/research/issue-2245-live-2026-11-24.md` with probes in `issue-2245-live-2026-11-24/`; index row; log entry.

## Done

* `continuity.py`: `demo_owner_override` keyed on `ZF_DEPLOYMENT_PROFILE=demo` (live demo runs `ZF_ENV=production`). `test_demo_owner_override.py` updated (old code fails it).
* Research note, probes, index row, log entry added.

Validation: `test_demo_owner_override` 2 OK; core restart-gate and suspension-drill suites 15 OK; api `test_exception_register` 45 OK; ruff clean; core mypy 3 pre-existing errors, same with and without the change. Tier: FULL by rule (src change); `rpi-checks.py --all` not run, the coordinator runs gates. Hosted CI not observed. No Azure change, nothing deployed.

## Per-criterion table

| Criterion | Proven / unproven | Basis |
| --- | --- | --- |
| Thread creation no 500 | Proven for this window (8/8 live 200); busy-lock 503 proven locally | probe-chat-result.json |
| Cause of the 2026-11-22 500 | Unproven (inference only) | Log Analytics denied |
| "Model calls: 1" visible | Unproven live | Root cause found and fixed in source; needs deployment (owner action) |
| Banner states rule-based mode | Proven live | banner JSON and screenshot |
| Which skills/routes call the model, why none did | Proven | override gated by ZF_ENV=production |
| Plain message when ask outlasts gateway | Proven locally | earlier test; not deployed |
