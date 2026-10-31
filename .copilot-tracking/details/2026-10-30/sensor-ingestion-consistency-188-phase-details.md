---
title: Sensor ingestion consistency phase details
ms.date: 2026-10-30
---

## Metadata

Task ID 188; slug sensor-ingestion-consistency-188.
Plan: .copilot-tracking/plans/2026-10-30/sensor-ingestion-consistency-188-plan.md.
Research: .copilot-tracking/research/2026-10-30/sensor-ingestion-consistency-188-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01 |
| P02 | Complete; lifecycle Review/final gate next | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Shared model and continuity contract

<!-- rpi:task id=P01-T01 -->
### P01-T01: Extend replay and implement statistical report

C1/C2: add keyword-only optional climate protocol and dated Measure tuple to
replay/descriptor. Use existing model validation and full-origin readings;
never restart RNG at the suffix. Preserve legacy descriptor/bytes when omitted.
Bind composed descriptor to climate manifest, model versions and dated history.
Report takes canonical observations and independent continuous reference,
handover UTC instant, cadence and explicit per-channel tolerances.
Require >=2 observations on each side per home/sensor, complete regular grid,
exact identity/provenance/units, finite numeric values. Compare actual/reference
mean step and per-side population standard deviations plus maximum point error.
Malformed evidence raises; numeric drift produces explicit failed metrics.
Completion: typed core tests including shifted values, dates and missing data.
Use independent per-channel point, mean-step and stddev tolerances with inclusive
`<=` comparisons. Test within/at/above nonzero boundaries, independently isolate
each metric, and reject negative/nonfinite limits (including boolean inputs).

<!-- rpi:phase id=P02 -->
## P02: Evidence and validation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Prove SQL handover, negative controls and replay

Depends on P01. Construct two granted homes including long stock ID; use
constructed changing climate and dated retrofit history. Write/read actual
composed CSV backfill, load prefix with shared admission, decode routed suffix
with actual SDK EventData and exact Binding, persist through SensorIngestion.
Query ordered per-home rows with independently configured units; compare to the
full reference. Reopen store/adapter and replay overlap/full window; require
unchanged durable rows/deliveries/DQ and accepted replay receipts.
Use existing fixture's ZF_SENSOR_MSSQL mode for real local SQL Server.
Extend src/api/checks/sensor_sql_check.py to select test_sensor_consistency
alongside its existing ingestion suite; this existing helper owns a random
loopback SQL Server, database, readiness and exact-container cleanup. Test must
assert backend mode; never use ambient configured SQL. Ordinary API discovery
and full gate alone do not prove this issue-specific SQL Server execution.
Extend the existing fake receiver test to cover the composed path where useful.
No transport mock establishes actual Azure transport.
Completion evidence: the locked task-owned SQL helper passed 46 tests, including
the explicit composed handover selector with MssqlStore backend assertion.
Both homes query twelve rows each; default zero-tolerance report passes; reopened
full-window replay retains 24 readings/deliveries and zero DQ, cases/audit unchanged.
The exact owned container was removed by the helper. API discovery passed
1,408 tests with 318 explicit skips; core/API Ruff/format/mypy passed.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Document, validate and prepare original Review

Depends on both preceding tasks. Owning core/API guides and existing IoT
synthesis/index/log must distinguish engineering from whole-issue acceptance.
Validation: focused semantic tests; API discovery with caller PYTHONPATH;
owning project Ruff check/format/mypy; full local gate after original Review
and local candidate commit. Heavy lock must cover each heavy command, with the
gate's own lock avoiding nested deadlock. Keep logs outside repository.
One independent review writes only its original review artifact; route later
findings without rerunning Review. Human/hosted/live approval remain separate.
Completion evidence records commands/exits/skips, exact commit and gate result.
Implementation completion: owning guides and synthesis/index/log updated,
targeted and requested validation passes recorded. Review, candidate commit
and complete gate are subsequent lifecycle gates, not implementation claims.
No full receipt or hosted/human approval is implied by checked implementation
markers. Original adverse critique remains unchanged.
