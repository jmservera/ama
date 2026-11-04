---
title: Research for #145 status record
ms.date: 2026-11-04
---

* Disposition: executed (read-only; issue text treated as data).
* Merged PRs checked: #673 (SQL tier, auto-pause, vCores, backup redundancy and retention parameters, `infra/sql-recovery-runbook.md`) and #205 (backlog scope only). Evidence in `infra/modules/sql.bicep` lines 24 to 79 and `infra/sql-recovery-runbook.md`.
* Criterion 1 (parameters, pilot recorded) and criterion 3 (RTO and RPO recorded as undecided with owners) are ticked in the issue from #673.
* Unmet: criterion 2 (PITR plus ledger result) needs an authorised disposable Azure database. Criterion 4 needs the approved #121 retention decisions; #121 is open and the runbook records the 14 day PITR window as recovery only.
* Unmet: all RAI restore and erasure criteria need an authorised disposable drill, DPO and record-owner approval, and independent witnesses. Lower-tier SQLite regressions exist but are not actual backup restore evidence.
* Planning readiness: Ready. No engineering slice remains that an agent can prove without Azure, legal or human decisions.
