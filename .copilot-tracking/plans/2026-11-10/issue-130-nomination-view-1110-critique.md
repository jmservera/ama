---
title: Issue 130 nomination read-only view plan critique
description: The single prospective critique of the final-candidate plan (issue 130), with direct dispositions
ms.date: 2026-11-10
---

## Execution

Executed once on 2026-11-10 by an independent read-only `rubber-duck` agent against the plan, details and research. Verdict: Proceed with changes. It is not repeated for this task.

## Findings and dispositions

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | Absent `nomination_records` cannot distinguish role-denied from an authorised case with no records (records are created lazily). | Blocking | Applied. Authorised is `challenge_targets` or `nomination_records` supplied by the server (removed together for denied roles, `store.py:472-479`, `projection.py:187-190`). Empty state for authorised, `null` for denied. Browser check asserts both. |
| 2 | Identity objects must not be stringified. | Non-blocking | Applied. Identity helper (name, role, "Unknown" fallback) and assertions. |
| 3 | Browser sequence cannot show a stale review with record, correct, review. | Non-blocking | Applied. Order is record, review, correct (stale), second review (current). |
| 4 | Challenge browser check and target size not scheduled. | Non-blocking | Applied. Existing challenge check run as impacted; rendered target-size assertions added. |
| 5 | Review outcome must not read as approval. | Non-blocking | Applied. Full outcome wording and a fixed not-approval note, asserted. |
| 6 | "No SQL" conflicts with the SQLite `ResidentApi` fixture. | Non-blocking | Applied. Plan states synthetic SQLite is used and is not SQL Server acceptance. |

No finding conflicts with a confirmed user decision; none required a user decision.
