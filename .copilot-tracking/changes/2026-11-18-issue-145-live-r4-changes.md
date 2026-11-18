---
title: Issue 145 live run 4 changes
ms.date: 2026-11-18
---

Refs #145. Docs-only, FOCUSED tier (no src, infra or workflow change; FULL tier not triggered; `rpi-checks.py --all` not run).

## Files

* docs/reference/research/issue-145-live-run4-audit-2026-11-18.md (new): audit note.
* docs/reference/research/issue-145-live-r4-raw-2026-11-18/ (new): redacted read-only `az` output.
* docs/reference/README.md: index row. docs/reference/log.md: appended entry.
* .copilot-tracking/: research, plan, details, critique, changes, review, state; the existing `issue-145-live-state.json` was modified in place (run 1 content stays in Git history).

## Witness note

`implement-start` was first refused (seq 4): "missing persisted artifact evidence: changes", because the state file lacked the changes pointer. The pointer was added and the call retried (seq 5, ok). Logs not edited.

## Azure

Read-only `az sql`, `az containerapp`, `az storage` and `az sql server show` calls. Nothing created or deleted; no throwaway resource exists. No credentials read.

## Per-criterion table (2026-11-18, demo)

| # | Criterion | Status |
| --- | --- | --- |
| C1 | SKU, auto-pause, redundancy parameters, pilot recorded | Proven in repo (ticked); sizing, region, zone placeholders are production-only |
| C2 | PITR performed, ledger verification recorded | Proven for the demo (runs 1 and 3) with limit: native `sp_verify_database_ledger` denied |
| C3 | RTO and RPO stated or undecided with owner | Proven (runbook: RTO undecided, owner named) |
| C4 | Backup redundancy and retention match #121 | Unproven, production-only (no #121 decision; #1906) |
| R1 | Actual backup restored with document and audit state | Partly proven (SQL yes; blobs not restored, no blob PITR) |
| R2 | Reconcile counts and history; reapply tombstones and holds | Partly proven (no hold state on demo) |
| R3 | No resurrection of revoked, suspended, erased or spent state | Unproven (no reapply code; tables empty; fix is FULL tier src change) |
| R4 | DPO and record-owner approvals | Not needed for the demo |
| R5 | Independent qualified witness | Unproven, production-only |
| R6 | Disposable restrictions, authorised exercise | Proven |
| R7 | Lower-tier evidence labelled | Proven (ticked) |
| R8 | Publish only hashes, status, counts | Proven (ticked) |

## Validation

* Relative-link check of the new note: all targets exist.
* `@` and GUID scan of raw files: none.
* `az bicep build` main.bicep and `build-params` prod, dev, pilot example: succeed.
* Git diff reviewed: docs and tracking only.
