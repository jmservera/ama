---
title: Issue 146 live changes record
---

Docs/evidence only; no src, infra or workflow change. Tier FOCUSED (basis: no source change). Documentation link and diff review; `infra/tests` unittest discover run (750 tests OK, 4 skipped); no mypy/ruff (no Python changed).

Files: docs/reference/research/issue-146-live-monitoring-rerun-2026-11-18.md (new), docs/reference/README.md, docs/reference/log.md, `.copilot-tracking` artifacts.

Live actions: throwaway metric alerts `tmp146b-job-failed` and `tmp146c-job-failed` created and deleted; no `tmp146` resource remains.

| Criterion | Proven or unproven | Reason |
| --- | --- | --- |
| C1 alerts: job failures | Partly proven | Throwaway rule on live failed-job signal fired (Total); not installed; Maximum shape did not fire in test |
| C1 alerts: poison queue | Unproven | No queue log category; storage blocks client; enabling is infrastructure change |
| C1 alerts: ledger digest | Proven | Installed, enabled, fired Sev1 (provoked by #115 test) |
| C1 alerts: IoT ingestion | Partly proven | Rule creatable earlier, not fired |
| C2 dashboard/workbook | Unproven | Not installed; private-link query blocks rendering |
| C3 runbook owners | Partly proven | 20 proposed-owner entries, tests pass; named people not appointed |
| T2 tokenomics dashboard with variance | Unproven | Same rendering limit; no cost export |
