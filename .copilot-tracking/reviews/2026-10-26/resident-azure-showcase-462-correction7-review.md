# Review record: correction 7 (#462), 2026-10-26
Execution: self-review after implementation; no independent reviewer was run. Independent review is left to the coordinator and hosted review.
Proved on real SQL Server (WITHOUT LOGIN users): clean view-only user passes verify_rights and the fresh database has only the two default public grants; a public SELECT grant on a user table, a public VIEW DEFINITION grant, a schema owner and a db_datareader member are each refused.
Not proved: external-identity SID check (fake only), Azure SQL differences, and ownership via other securable kinds beyond schemas, objects, types, XML collections and owned principals. Outcome: open items recorded; no material finding closed by assertion.
