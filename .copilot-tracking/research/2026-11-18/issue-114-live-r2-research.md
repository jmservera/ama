---
title: Issue 114 live rerun research (r2)
ms.date: 2026-11-18
---

# Research (opening, rerun r2)

* Task: issue-114-live (rerun). Refs #114. Branch test/sql-ledger-live-20261118T1051Z.
* Prior evidence on main: docs/reference/research/sql-ledger-live-2026-11-18.md (PR #1932) proves load, latency, cost and PITR plus erasure re-application at demo scale. Open residuals there: per-year reliance check not run on the deployed image, native ledger verification not run, tamper detection not shown on live data.
* Plan for this rerun: read-only live checks on `retrofit` from a throwaway Container Apps job (orchestrator image, existing identity); tamper detection on an in-memory copy of live audit entries; local test suite re-run. No source change, no write to `retrofit`.
* Planning Readiness: Ready. Research disposition: executed (reuse of prior evidence plus new live probes).
