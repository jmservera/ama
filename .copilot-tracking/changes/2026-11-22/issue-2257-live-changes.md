---
title: Issue 2257 changes
ms.date: 2026-11-22
---

Classification: FULL tier by rule (source change in `src/api` web UI); the complete gate is run by the coordinator, never here. Local checks run: `test_workspace_scripts`, `test_accessibility_baseline`, `test_content_standard`, `test_app_wide_ux`, `test_case_journey` (124 tests, OK).

## Changes

* `src/api/src/zava_forward/api/web/app.js`: `fetchReadRetrying` retries a transport failure on reads twice (400 ms, 1200 ms), shows "The connection dropped. Trying again.", stops on abort.
* `src/api/tests/test_workspace_scripts.py`: network failure now recovers, is bounded and clears status.
* Research note, probe scripts and results under `docs/reference/research/`; index and log updated.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Map retries or recovers without a reload | Proven for the patched client; deployed client still fails, deployment is not done | `recovery-proof-result.json`, unit test |
| Cause is found | Unproven at request level; supported by log timing (probe timeouts, scale-in 14:56:51) | research note |
| Failure reproduced live | Unproven: 8 of 8 passed now (S3); injected reset reproduces the message | `probe-result-155403.json` |
| Azure estate unchanged, no throwaway resources | Proven: read-only `az` and log queries only | this record |
