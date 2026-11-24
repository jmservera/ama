---
title: Issue 2244 live r15 critique (single pass)
ms.date: 2026-11-24
---

Candidate: read-only `_migrate_current` for MssqlStore with a read-only `continuity.gate_in_sync` helper.

| Risk | Disposition |
| --- | --- |
| Fast path skips a needed repair | Conservative: any mismatch, missing row, unparsable continuity document, or missing `gate_version` returns False and takes the unchanged locked path. Applied. |
| Gate epoch or holds drift silently | Compare `gate_sync_rows` output with stored epoch and the stored hold rows; any difference takes the locked path. Applied. |
| SQLite behaviour changes | Override is on MssqlStore only; the shared SqlStore body is refactored only to expose the identity-drift read (behaviour preserved). Applied. |
| Race: another replica migrates between check and skip | Same race existed for the schema check; the locked path remains authoritative whenever the read says not current. Accepted. |
| Live proof needs a real SQL Server | Use the throwaway copy and delete it afterwards. Applied. |

Verdict: proceed. No conflict with confirmed owner decisions.
