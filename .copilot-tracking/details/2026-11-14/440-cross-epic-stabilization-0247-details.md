---
title: Cross-epic stabilization journey phase details (#440)
ms.date: 2026-11-14
task_id: 440-cross-epic-stabilization-0247
---

## Phase 1: integration test module

File: `src/api/tests/test_cross_epic_stabilization_journey.py`. One local HTTP server over a `SqlStore` built from the synthetic `DATA` fixture, signed in as the first staff user.

* #165 `test_synthetic_provenance_and_anchors_reach_the_workbench`: manifest passes `record_issues` and `emission_issues`; name and home fields are pattern-clean with lat/lon 0 anchors; a missing label and an email-like value are detected; dataset hash and source revision are stable; cases load through `/api/cases` and `/api/me` shows the synthetic progress scope.
* #104 `test_assistant_proposal_is_bounded_attributed_and_read_only`: proposal is `Proposed`, `template`, no model, at most n items, each with citations and plain reasons; staff case, gate, hazard, funding, document and history views are unchanged afterwards.
* #104 `test_ai_unavailable_fails_closed_to_manual_workflow`: `ai` and `workflow-only` modes return the deterministic template with a fallback reason; chat storage is refused with 403 and status shows disabled, one call, no retries, no memory; state unchanged.
* #149 `test_workbench_keeps_non_colour_plain_language_and_manual_cues`: skip link, polite status region, glyph cues for danger, ok and wait, reduced motion, workflow-only labels, manual-path copy and navigation scopes.

Typing: every function, parameter and local is annotated; one `type: ignore[no-untyped-call]` covers the untyped `App` constructor.
