---
title: Quality sensor demo 1288 C8 recovery details
ms.date: 2026-11-09
---

Written 2026-11-09T08:05Z with the C8 plan, before any edit.

## Files

* `src/api/tests/test_assistants.py`: `MssqlFixture.setUp` drop list gains `assistant_schedule` and `assistant_dispatch_gate`, plus the C7 transient tables if present.
* No product source change planned.

## Commands

* `docker run` owned container `zf-1288-sql` under `flock -n /tmp/ama-rpi-heavy.lock`; `python -m unittest discover -v -s tests -p <file>` from `src/api` with `ZF_TEST_MSSQL=1`, loopback SQL and `PYTHONPATH=../core/tests:../agents/tests`.
