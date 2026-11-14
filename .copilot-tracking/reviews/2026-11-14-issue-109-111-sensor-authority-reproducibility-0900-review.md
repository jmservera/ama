---
title: Sensor non-authority and reproducibility review (Refs #109, #111)
date: 2026-11-14
---

Review executed once. Outcome: conformant for the stated criteria, with routed follow-ups.

## Assessment

* #109 criterion 3: proven by `test_sensor_non_authority_boundary.py` for retained readings, analysis, candidates and an approved synthetic draft. Boundary covers hazard state, service clocks, hazard and legal holds, case data and ranking. SQLite only.
* #111 criterion 1: proven by `test_sensor_analysis_reproducibility.py` over retained readings; one real gap (row-order dependence) fixed.
* Not a statement that an approved rule, live policy or human signoff exists.

## Routed follow-ups

* Run the new suites against SQL Server (`ZF_SENSOR_MSSQL=1`); they skip there.
* Consider speeding the reproducibility suite (ingest dominates runtime).
* Post-merge: tick #109 criterion 3 and #111 criterion 1 once hosted CI is read.
