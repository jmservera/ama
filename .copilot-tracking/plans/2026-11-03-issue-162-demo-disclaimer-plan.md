---
title: Issue 162 demo-only disclaimer plan
ms.date: 2026-11-03
---

Details: [phase details](../details/2026-11-03-issue-162-demo-disclaimer-details.md). Single slice; no stack needed.

* [x] Phase 1: add `DEMO_BASIS` and `DEMO_DISCLAIMER` to `chat_isolation.py`; put `basis` in granted and refused audit entries and the disclaimer in the granted response. Default deny and metadata-only unchanged.
* [x] Phase 2: extend `test_break_glass_is_default_deny_audited_and_metadata_only`.
* [x] Phase 3: add the dated policy record, link it from the DPIA record, core README, reference index and log.
* [x] Phase 4: focused tests, ruff, mypy; open PR with `Refs #162`.

Critique (single pass, executed): verdict proceed. Advice to enable break-glass by default or to allow content access is rejected: the owner approved a disclaimer, not content access or a default-on endpoint.
