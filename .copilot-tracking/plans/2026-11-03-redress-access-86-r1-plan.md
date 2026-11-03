# Plan: redress access under holds test (Refs #86, R1)

Research: [research](../research/2026-11-03-redress-access-86-r1-research.md). Details: [details](../details/2026-11-03-redress-access-86-r1-details.md).

* [x] Phase 1: add test that Complaint and Independent review open under withdrawal, disputed authority, tenure hold and expired retention
* [x] Phase 2: focused validation (test file, ruff, mypy)

Tier: focused. Test-only; no security, infrastructure, SQL schema or deployment change; no gate run.

Critique (single pass, author-recorded): keep production code unchanged because the test passed first time (applied); do not claim criterion 4 (applied).
