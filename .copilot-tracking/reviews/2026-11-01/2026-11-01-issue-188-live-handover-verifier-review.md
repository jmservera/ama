---
title: Issue 188 live handover verifier review
ms.date: 2026-11-01
---

* Changes: ../../changes/2026-11-01/2026-11-01-issue-188-live-handover-verifier-changes.md
* Review execution: executed once, self-review of the diff after implementation. Outcome: conformant for the stated scope; criteria not newly proven.
* Findings: (1) `--replay-check` writes to the store; documented in help text and README, off by default. (2) Reads use the assistant connection and no secrets are handled; Azure auth stays in `ZF_STORE=mssql` configuration. (3) Mean-step/spread tolerances are caller-declared, not new operational thresholds.
* Acceptance mapping: all three criteria stay locally proven only (#587) and unmet for actual Azure SQL live streaming; the PR therefore uses `Refs #188`.
* Routed follow-up: run the verifier on Azure SQL after a live Hub stream (needs owner-provisioned Azure, #110, #140).

## Post-review correction (PR 645 Copilot threads)

* Five findings accepted and fixed: non-initializing read-only store open, window-bounded observed series, replay of retained stored payloads, 100-row replay batches, `home_key` home validation with the 64-unit bound. See the changes artifact. Review outcome for the original assessment is unchanged; SQL Server and Azure SQL remain unexecuted.

## PR #645 Copilot review follow-up (2026-11-01)

Two valid findings fixed: retained accepted payload and accepted calibration returned for consumer-managed readings, and reference rows validated before window bounds. Focused sensor tests (core 37, api 85) and ruff pass. Independent exact-head review and the complete local gate remain required before merge.

## PR #645 second Copilot review follow-up (2026-11-01)

Two valid findings fixed: batched witness lookup limited to selected readings, and a truncated-reference regression that now reaches `_windows` validation. Focused tests and ruff pass. Independent exact-head review and the complete local gate remain required before merge.
