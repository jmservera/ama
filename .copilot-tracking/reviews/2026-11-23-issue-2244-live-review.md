# Review 2244 live (2026-11-23)

Executed once, after implementation. Outcome: conformant for the stated scope, with open items routed to follow-ups.

* Fast paths are read-only, fall back to the unchanged locked path on any missing object, and keep the ledger error in the locked path. No SQLite behaviour changed (the override lives in `MssqlStore`).
* Residual risks: index existence matches by name across the database (names are table-prefixed); `_migrate` and `_migrate_recommendations` still lock; probe budget is below the worst-case retry wait; full core suite summary not captured; change not deployed or exercised against real Azure SQL.
* Follow-ups: 1 owner deploys the fix and re-checks start under contention; 2 align the StartUp probe with the retry budget (production setting); 3 read-only precheck for `_migrate` and `_migrate_recommendations`.
