# Plan: resident demo authority to 31 December 2027 (Refs #521)

Slice 1 (this PR, source only): move the shared cap, tests and docs. Slice 2 (stacked, later, owner-gated): live Azure apply and verification.

* [x] Phase 1: set `maximum_expiry_utc` to 2028-01-01T00:00:00Z
* [x] Phase 2: update tests so earlier cutoffs (2026-11-01, 2027-02-01) are accepted where valid and the new limit plus one second is refused
* [x] Phase 3: update infra and API READMEs, knowledge-base index and log, with cost and rotation notes
* [x] Phase 4: focused tests, ruff, mypy

Details: [details](../details/2026-11-03-demo-authority-521-r1-details.md). Critique: single pass, no conflicts with the owner decision; tariff scope kept out. No security, infrastructure, SQL-schema or deployment change in the slice; the focused tier applies. Azure is untouched.
