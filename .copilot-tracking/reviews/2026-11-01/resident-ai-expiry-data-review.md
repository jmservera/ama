# Review: resident AI expiry as data (issue 624)

Execution: executed once. Outcome: conformant, no open material findings.

* AC1 expiry column, idempotent, default, read by reserve: met (`complete` has no expiry logic).
* AC2 tests set future expiry, refusal-after-expiry proven: met, passing locally against real SQL Server.
* AC3 README documents read/extend; Python `EXPIRES` consistent and documented: met.
* AC4 no live extension: met; no Azure access.

Follow-up (not in scope): optionally have the Python gate read the SQL expiry; independent human review and hosted CI mssql check remain pending.
