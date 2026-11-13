---
title: Plan for #216 citation and card link resolution regression
ms.date: 2026-11-12
---

* Research: ../research/2026-11-12-issue-216-link-resolution-2236-research.md
* Details: ../details/2026-11-12-issue-216-link-resolution-2236-details.md

## Phases

* [ ] P01 Add the link-resolution regression to `src/api/tests/test_regulatory_chat_api.py`
  * [ ] P01-T01 Helper that resolves each citation and card link over loopback and compares id, version, hash, status, quote prefix, truncation flag and card provisions
  * [ ] P01-T02 Test over base, long-text and conflict scenarios
  * [ ] P01-T03 Negative controls: swapped provision link and dangling card link fail
* [ ] P02 Validate: targeted api tests, ruff check and format for the file, git diff review
* [ ] P03 Record changes evidence; one Review

## Out of scope

Thresholds, grader, staff trial, cost, model calls, README gate semantics, scorer changes, production code.
