---
title: Issue 82 quality rule provenance plan (2026-11-05, increment 4)
ms.date: 2026-11-05
---

* [ ] Phase 1: change `QUALITY_RULE.source` only (details: `../../details/2026-11-05/issue-82-rule-provenance-details.md`).
* [ ] Phase 2: extend the existing `test_quality_gate_outcomes_and_rule` with one provenance assertion; run focused gate and quality tests, configured ruff and mypy with external caches.
* [ ] Phase 3: Changes, a dedicated canonical Review, commit locally.

## Critique (single pass, self-run)

* Risk that the string is a stored or hashed contract: checked, it is not (research). Applied: proceed as an annotation.
* Dropping the BRD citation: BRD FR-008 is material-change invalidation, not applicable; retaining it would repeat RV-001. Applied: remove it, record reason here.
* No invented values. Applied: reviewer, date and version unchanged.
* No trivial constant-restatement test: assert only that the source names the PRD document path and FR-008 and not the BRD FR-008 mis-citation, in the existing test. Applied.
* Tier FOCUSED, stop to FULL if behavior changes.
