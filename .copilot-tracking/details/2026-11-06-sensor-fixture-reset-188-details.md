---
title: Details for #188 sensor test-fixture reset isolation
ms.date: 2026-11-06
---

* Files: `src/core/tests/sensor_consumer_fixture.py` (reset), `src/core/tests/test_sensor_consumer_live.py` (one regression). External only after freeze: `/tmp/188-sql-readiness-r14/{wrapper.py,wrapper.r12-to-r14.diff,HANDOFF.md}`.
* Acceptance: (1) reset=True leaves no consumer-table rows from an earlier store on the same state, on SQLite now and on owned MSSQL when admitted; (2) reset=False and reopen preserve rows and witnesses; (3) the regression is RED before and GREEN after on SQLite; (4) no runtime, schema, assertion, expected reason, selector or threshold change; (5) existing constructed modules still pass with zero skips.
* Test design: behavioral isolation and reopen preservation through the real `SensorConsumer` and `retained_envelopes`, not constants or framework behavior.
* Controls: legacy and weather rows remain handled by existing tests; the refusal and idempotence assertions are unchanged.
* Disposable endpoint constraints (later, admitted wrapper only): run-owned loopback container, random label, exact CID cleanup, 3 GiB and 2 CPU, password only in memory. Reset touches only that database. Foreign `sharp_margulis` is never touched.
* Chronology: the original ingest was post-hoc; the weather loop and r9/r10 were prospective; r11 HANDOFF planning was not prospective; r12 and r13 were executed as recorded. This record is written before any test or helper edit.
* Not claimed: whole-188, statistical, live, owner or calibration acceptance; FULL on the new head.
