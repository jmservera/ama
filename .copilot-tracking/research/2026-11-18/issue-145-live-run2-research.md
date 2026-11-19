---
title: Issue 145 live run 2 research (opened 2026-11-18T10:55Z)
ms.date: 2026-11-18
---

# Research: issue 145 live run 2

* Task: for each unticked criterion of #145, prove with recorded evidence or state why not provable on the demo. Earlier run artifacts (`issue-145-live-*`, same date) are preserved unchanged; this run uses the `run2` suffix.
* Authority: owner decisions 2026-11-18 (demo, desktop, resource group `ama`, cap USD 700, no drills on the live DB, no Key Vault rotation, no production change).
* Existing evidence: `docs/reference/research/issue-145-live-pitr-restore-evidence-2026-11-18.md` (PITR of `retrofit` to `retrofit-pitr145`, deleted) and `sql-ledger-live-2026-11-18.md` (#114 drill).
* Disposition so far: `reused` for the PITR and drill evidence; fresh read-only re-verification of Azure state planned.
* Planning Readiness: Ready. The re-verification and the code check are complete; the outcome is in the run2 re-verification note.
