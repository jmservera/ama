# Issue 116 live changes (2026-11-20)

Status: complete. Tier classification: FULL applies (file under `src/` changed, test only); the complete gate is not run here and stays with the coordinator.

## Changes

* `src/core/tests/test_ai_provider_payload_spy.py`: added `test_proactive_task_sends_the_same_closed_payload`.
* `docs/reference/research/issue-116-live-r5-evidence-2026-11-20.md`, `docs/reference/README.md`, `docs/reference/log.md`.

No product code changed; no defect found. No Azure resource created or changed; nothing to delete; credentials not read.

## Validation

Spy module 15 OK; core boundary set 73 OK; api 135 run, 1 skipped; agents chat model 17 OK; call-site inventory 6 OK; mutation check catches a dispatch leak; mypy 23 errors equal to baseline; ruff clean. `test_assistants_dispatch` not runnable (no `opentelemetry`).

## Per-criterion table

| Criterion (issue 116) | Status | Evidence |
| --- | --- | --- |
| Every role tested against every endpoint | Ticked previously; proven offline (r4: 41 tests) | round 4 note |
| Contractor view has no vulnerability reason anywhere | Ticked previously; r4 override fix | round 3 and 4 notes |
| Free-text redaction approach decided | Ticked previously | not re-examined |
| Reason roles confirmed (OD-14, OD-19) | Ticked previously; owner decision 2026-11-18 | round 4 note |
| Allowlists at every provider boundary | Proven offline for each enumerated boundary; unproven live (payloads not observable) | round 5 note |
| Provider-spy exact payload tests | Ticked previously; 15 spy tests OK | round 5 note |
| Unknown task, excess input refused before provider | Ticked previously; bounds tests OK | round 5 note |
| Recheck permissions on outputs and exports | Ticked previously; partial live proof for one role only | round 3 |
| Document AI needs derivative or exception | Ticked previously; `LookAtBodies` OK | round 5 note |
| Source permissions, consent, manual routes | Ticked previously | not re-examined |
| Reuse current wrappers | Ticked previously; call-site inventory OK | round 5 note |
