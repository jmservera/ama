<!-- markdownlint-disable-file -->
# Plan: issue 1238 C3 audit payload provenance (1110)

Prospective, written 2026-11-10T01:00Z before any test or source edit.
Research: [research](../../research/2026-11-10/issue-1238-c3-audit-payload-1110-research.md).
Details: [details](../../details/2026-11-10/issue-1238-c3-audit-payload-1110-details.md).
Critique: [critique](issue-1238-c3-audit-payload-1110-critique.md).

## Phases

* [x] Phase 1: one critique before tests or source.
* [x] Phase 2: red regressions (evidence substitution, binding restamp,
  legacy generic entry) on JSON, SQLite and MSSQL.
* [x] Phase 3: implement the payload digest and verification.
* [x] Phase 4: validate (module, selected MSSQL under one nonqueued
  admission, Core and API mypy, Ruff, README).
* [x] Phase 5: one Review, commit, handoff.

Boundaries: only resident_decisions.py, its test file and the Core README;
no shared store, server, schema, binding population or approval.
