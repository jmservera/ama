---
title: Quality sensor demo 1288 C3 review
ms.date: 2026-11-08
---

Recorded 2026-11-08T21:01Z. One self-review, executed once; outcome partial because heavy gates are pending. Boundary: C3 diff over `8d95ae96`.

## Execution and outcome

* Execution: done, author self-review against the six findings and light suites in the changes artifact.
* Outcome: source and light SQLite evidence conform; SQL Server, browser and FULL not run.

## Findings

* Fail-closed choices: ambiguous authority is "requested"; a count mismatch makes consent unknown; verify/accept refused while withheld.
* Risk: the `_due` exact-id lookup runs one extra indexed primary-key read per eligible case.
* Risk: `migrate` swallows index reconcile errors with a warning; readers still fail closed.
* Overlap: `sensor_consumer.py` also changed by #184; semantic merge needed.
* Not shown: tests are SQLite only. MSSQL DDL path (`ensure_control_home`) is unexercised.

## Ranked follow-ups

1. Admitted FULL, SQL Server variants and query plans, then browser/axe.
2. Semantic merge with #184 after it lands.
3. Release, attestation, finite allowance, separate live exercise.
