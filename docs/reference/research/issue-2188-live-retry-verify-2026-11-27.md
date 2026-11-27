---
title: Issue 2188 live, forged retry records rejected by receipt verify (2026-11-27)
description: validate_retries accepted a retry row with no log hash; it now requires a 64-hex hash that matches a hashed log in the receipt; per-criterion status
ms.date: 2026-11-27
---

Scope: synthetic demo, desktop only. Change in `tools/rpi-checks.py` and `tools/test_rpi_checks.py`; no `src/` change, no Azure access, no `rpi-checks.py --all`. Tier: focused (stricter verification only, no permission, image, package or gate-semantics loosening).

## Gap

`validate_retries` compared `files.get(log) != row["sha256"]`. A row with `sha256: null` and no entry in `files` made both sides `None`, so verify accepted a retry that pointed at no hashed log. Reproduction at head: `validate_retries({"retries":[{"group":"x","log":"0001-x.log","sha256":None,"exit_code":1,"argv":["a"]}],"files":{},"commands":[]})` returned without error.

## Change

* The row's `sha256` must be a 64-character lowercase hex string, which also forces the log to be present in `files`.
* The tamper test gained three cases (null hash with no file, short hash that matches `files`, log missing from `files`). It failed before the fix (`GateError not raised`) and passes now.
* `python3 -m unittest tools.test_rpi_checks`: 134 tests OK (74 s). `ruff format --check` clean; `ruff check` reports the same 19 findings with and without the change.

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| Drop `--no-cache` | Proven (unit level) | earlier notes; 70.5 s to 7.2 s on one image |
| Four concurrent image builds | Proven at scheduler level only | image-concurrency note |
| Shard API tests | Proven (unit level) | `shard_partition` tests |
| Retry a failed class once, recorded | Proven at shard level; not test-class level | `receipt["retries"]` |
| Receipt records retries | Proven (unit level) | timing-retries note |
| Verify still rejects tampered evidence | Proven (unit level), retry-record hole closed here | `test_validate_retries_rejects_tampered_or_forged_records` |
| Wall time before and after, same tree | Unproven | needs two full gates; `--all` is forbidden for this worker |
