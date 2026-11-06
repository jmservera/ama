---
title: Changes for #188 live-sim handover omission correction
ms.date: 2026-11-05
---

* Reproduction before the fix (head 40e6a35f4): the new refusal test failed with `ValueError not raised`; the earlier test showed `passed=true` while the live row was excluded from statistics.
* Modified `src/api/src/zava_forward/api/sensor_handover_verify.py`: refuses `HANDOVER_SCHEMA_UNSUPPORTED` (exit 2) when the home/window holds a live-sim row, before any replay write.
* Modified `src/api/tests/test_sensor_consistency.py`: replaced the combined test with raw-replay, refusal and legacy-only tests.
* Modified `src/api/README.md`: documents the refusal and the unapproved future weather-to-weather contract.
* Preserved: lossless `retained_envelopes`, indoor-analysis exclusion, thresholds, consent and calibration controls. Prior slice artifacts are unchanged.
* Validation: api `test_sensor*.py` 92 OK; core `test_sensor*.py` 181 OK (1 skipped); ruff and mypy results below in the review.
* Remaining C2 scope (source-specific): live-to-backfill statistical handover is NOT demonstrated. It needs a versioned weather-to-weather reference/continuity contract (research), SQL Server and live Hub to Azure SQL runs (owner-gated, #110), and the FULL gate. No acceptance is claimed and no criterion is ticked.
* FULL gate pending; the earlier failed receipt `/tmp/rpi188-full-20261105T0740/receipt.json` is preserved untouched. #96 PID 1232396 holds heavy resources; nothing was queued.
* Clean freeze: 94 ignored own-generated files (78 `.pyc` with sibling sources, 16 Ruff cache files, all created this session) were listed in a finite manifest, archived and restored to new external scratch with matching SHA-256 before removal. Archive, manifest and prune journal: `~/.local/share/ama/tracking-archives/2026-11-05-i188-cache-189d5f/`. Only those files and their emptied directories were removed; no tracking, private, original or adverse input was touched. Probes used external caches (`--no-cache`, mypy `/tmp/mypy-188`) and `PYTHONDONTWRITEBYTECODE=1`.
