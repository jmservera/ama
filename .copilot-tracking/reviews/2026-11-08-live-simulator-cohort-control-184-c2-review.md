---
title: "Review: #184 correction 2"
ms.date: 2026-11-08
---

Execution: self-review run once, bounded to the C1 High finding. Independent
exact-head assessment belongs to the coordinator. Outcome: the finding is
addressed in source with regression and SQL evidence; this is not a conformance,
live-receiver, model/Quality or closure claim, and no criterion or approval is
ticked.

## Checked

* Control is validated before any persistence object exists (tests: stopped,
  expired, sub-second, invalid refuse with no persistence call).
* `ZF_STORE=mssql` no longer builds `MssqlStore`; the connector runs no DDL,
  seeding, metadata or queue set-up.
* Every runtime statement of `SensorConsumer.process` is covered by the
  documented grants; the unused `sensor_register` grant was removed.
* C1 cohort and stop behaviour and the retained-reading contract are unchanged.

## Remaining and residual (Refs #184, #110, #189)

* `sensor_consumer.py` is shared with #1288 (Quality logic); only the
  constructor changed, but a textual merge may be needed. The file's
  pre-existing format drift was left alone.
* `acknowledge`, `configure` and schema provisioning remain a setup/admin task
  with no deployed job here; who provisions the schema in Azure is undecided.
* Not delivered: Azure grants, routing-ready, live activation, Hub-side key
  hygiene proof, in-app admin screen, child stories #185/#188/#189, B1 price
  verification.
