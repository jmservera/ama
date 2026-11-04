---
title: Plan for #74 home case browser evidence slice
ms.date: 2026-11-04
---

* [x] Phase 1: add `src/api/checks/home_case_browser_check.py` (details: ../details/2026-11-04-74-home-case-browser-evidence-details.md).
* [x] Phase 2: render cost allocation in plain language instead of JSON and cover it in `test_home_case_api`.
* [x] Phase 3: README note, focused tests, ruff, mypy with tests, node check.
* Stacked follow-ups: version-recording form, building record versioning, hosted CI wiring of the check, independent review.
* Critique: one self-run pass. Applied: check is read-only and asserts no non-safe requests; no workflow change (coordinator owns CI); axe is optional and hash-pinned.
