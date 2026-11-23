---
title: Changes for issue 2188 live evidence refresh
date: 2026-11-22
---

## Changes

* docs/reference/research/issue-2188-live-gate-speed-2026-11-22.md: new note superseding the retry finding of the 2026-11-21 note.
* docs/reference/README.md and docs/reference/log.md: index and log entries.
* No `src/` or `tools/` change; Azure estate untouched; throwaway docker tags `ama2188b:fresh` and `ama2188b:layer` removed.

## Validation

* `python3 -m unittest tools.test_rpi_checks tools.test_rpi_gate_timing`: 144 tests OK.
* Timed api image build: fresh 70.5 s, layer 7.2 s (warm best case).
* Tier: FOCUSED (documentation only, no gate semantics changed). `rpi-checks.py --all` not run; hosted CI for the exact head is not observed because nothing is pushed.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Wall time measured before and after on the same tree | Partly proven | image build pair measured; gate-level pair unproven (needs two full gates) |
| Receipt records retries | Proven (unit level) | `receipt["retries"]`, `validate_retries`; no live full-gate receipt with a retry |
| Verify still rejects tampered evidence | Proven (unit level) | 144 tests OK incl. tamper tests; no full-gate receipt verified here |
| Drop `--no-cache` (issue text) | Proven in code | `image_build_argv`; full tier keeps fresh |
| Four images concurrent (issue text) | Unproven, not implemented | `docker_lock` serialises images |
| Shard api tests (issue text) | Proven in code | 89/90/89 modules over three shards |
