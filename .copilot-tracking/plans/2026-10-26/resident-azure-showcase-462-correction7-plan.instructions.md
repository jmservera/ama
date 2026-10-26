# Plan: correction 7 (#462), 2026-10-26

1. Split verify_principal into identity plus verify_rights; add an ownership predicate (schemas, objects, types, XML schema collections, owned principals); allow only default public grants (database scope CONNECT and the two VIEW ANY COLUMN ... KEY DEFINITION; sys/INFORMATION_SCHEMA objects), document this.
2. Add opt-in real-SQL tests: clean pass, public table grant, public database-scope grant, schema owner, db_datareader member. Run against a local throwaway mssql container under the heavy lock; remove it.
3. demo.js: after sign-out focus the sign-in heading and announce "You have signed out."
4. Run tests, mypy strict, ruff, node --check; reply on threads; one commit.
Details: see research note. Critique: self-recorded in the review file; no independent subagent critique (disclosed).
