# Plan: tenure verification and decision route (Refs #131, R2)

Research: [research](../research/2026-11-03-tenure-route-verification-131-r2-research.md). Details: [details](../details/2026-11-03-tenure-route-verification-131-r2-details.md).

* [x] Phase 1: add `tenure_verify` action in resident_decisions.py
* [x] Phase 2: core and API tests
* [x] Phase 3: core and API READMEs
* [x] Phase 4: focused validation (unit, ruff, mypy)

Tier: focused. Resident-record code only; no infrastructure, SQL schema, deployment or security control change; no gate run.

Critique (single pass, author-recorded): keep hold unchanged because enumeration of all households (C1) and Finance cost are not evidenced (applied); require Legal reference before a route (applied); verifier must differ from recorder and be a data owner role (applied).
