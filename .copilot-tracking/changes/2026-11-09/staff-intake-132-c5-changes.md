---
title: Staff intake 132 C5 changes
---

Cycle 5 of 5 (final default correction). Refs #132.

## Changes

* `staff_intake._worker(new=True)` rejects any registered staff email, code or oid as worker for new capture.
* `staff_intake._read_dependency` installs the existing `procurement_validation` token (snapshot read first
  under `store.lock`), holds `store.dblock`, refuses an existing token and always clears its own.
* `capture` wraps `submit_quality` in it. No change to sqlstore, procurement or quality.
* Tests: staff identifiers (code, email, mixed case, contractor code), staff name denied by the real accept
  route, replay and correction after registration, two-store withdraw and reissue interleaves, unrelated
  commit success, existing-token refusal.
* Ordinary merge `c0b1cf12b` of parent a8593a7a, clean, no conflicts.

## Evidence

* Red: /tmp/zf132-c5-red.log (3 failures; token test hung until the test was corrected).
* Green: /tmp/zf132-c5-green.log, /tmp/zf132-c5-api.log (200 ok, 34 skipped env-gated), /tmp/zf132-c5-core.log
  (146 ok), /tmp/zf132-c5-mssql.log (30 ok, real SQL Server, lock free, exit 0).
* ruff and strict mypy clean.

## Divergence

* Test bug fixed in-cycle: the sentinel token is cleared by lock exit, so the test asserts a 409 and no receipt.
