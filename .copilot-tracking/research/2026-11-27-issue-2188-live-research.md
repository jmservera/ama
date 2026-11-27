# Research: issue 2188 live (2026-11-27)

Disposition: executed. Planning Readiness: Ready. Tier: focused (tools/ and docs only, no src change).

Prior notes read: docs/reference/research/issue-2188-live-*.md (speed, image concurrency, wall time, timing retries). They cover timing, scheduling, sharding and the timing tool.

New angle: `validate_retries` in tools/rpi-checks.py compares `files.get(log) != row["sha256"]` but never requires `sha256` to be a 64-hex string.

Reproduction (before the fix): a retry row with `sha256: None` and `files: {}` passes `validate_retries`, so verify accepts a forged retry that points at no hashed log. Output: `ACCEPTED forged retry with no log`.

Impact: the criterion "verify still rejects tampered evidence" has a hole for the retry record; a receipt could carry retry evidence with no log on disk.
