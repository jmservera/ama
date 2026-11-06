---
title: Changes for #188 current-main preparation
ms.date: 2026-11-05
---

* Ordinary no-ff merge of origin/main bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f into the child (merge commit 521e33dfd0d415bfbeb4fe56223d00303d5d48d5, tree f9aee5e55a8e0394f8f2909b22b7c1d4024d89bc; parents 834e2becf and bb3a3b03c). No conflicts, no source edit, no rebase, amend, force or retarget. Parent feat/live-simulator-integration-184 remains ead177ef90d24666557708ea344848a1be43bdf8.
* Import proof: with explicit worktree source paths (no mvp), `zava_forward.core.sensor_consumer` and `zava_forward.api.sensor_handover_verify` resolve under /home/azureuser/source/ama-wt/i188/src. The installed distributions resolve to /home/azureuser/source/ama, so bare imports would test another checkout.
* Focused regressions (PYTHONDONTWRITEBYTECODE=1): `test_sensor_consistency.LiveEnvelopeReplayTests` (raw replay, HANDOVER_SCHEMA_UNSUPPORTED refusal for library, replay and CLI, legacy-only pass), `test_sensor_consumer_live`, `test_sensor_analysis_store`: 21 tests OK, 0 skipped, exit 0. A first invocation failed to import for a missing tests path in my PYTHONPATH (exit 1, 19 tests, 1 import error); it was a command error, corrected and rerun. The earlier 1-skip qualification belongs to the broader core sensor suite, which was not rerun; it is preserved, not cleared.
* `ruff check --no-cache` and `ruff format --no-cache --check`: src/api and src/core exit 0. mypy with external caches /tmp/mypy-188 and /tmp/mypy-188-core: api 24 and core 127 source files, no issues.
* Not run: full or partial gate, browser, SQL Server, Docker, scan, cloud, private data. No cleanup. Heavy lock is owned by #96 runner 1592594; nothing queued.
* Preserved: lossless `retained_envelopes`, indoor `observed_series` exclusion, refusal before statistics and replay, legacy-only behavior. No weather-to-indoor conversion, calibrated invention, threshold, schema, consent or adapter change. Raw replay and idempotence are not statistical or physical acceptance; C2 continuity is unproven and the weather-to-weather scope question stays pending.
* Missing evidence: FULL local receipt (admission order 96, 440, 233, 144 is the coordinator's), independent exact-head review, hosted CI for this head (PR 1203 published contexts are for the older c9a14573d).
