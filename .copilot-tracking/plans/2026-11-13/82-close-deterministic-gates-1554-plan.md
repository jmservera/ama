---
title: Issue 82 deterministic gates plan
ms.date: 2026-11-13
---

## Plan

* [ ] P1 Add `ELIGIBILITY_RULE`, `AUTHORITY_RULE`, `FINANCE_RULE` (unreviewed exercise fixtures) and `eligibility_gate`, `authority_gate`, `finance_gate` in gates.py.
* [ ] P2 Add `CONTROLLED_RULES` registry covering every `GATE_KINDS` entry.
* [ ] P3 Wire `finance._fin_commit_raise` and `grants.require_authority` denials through gate results (same exception types and text).
* [ ] P4 Tests in `test_gates.py`: registry completeness and metadata, unknown never passes for each new gate, wiring unknown/fail/pass.
* [ ] P5 Run core and api tests, ruff, mypy; independent review; commit.

Details: [details](../../details/2026-11-13/82-close-deterministic-gates-1554-details.md)
