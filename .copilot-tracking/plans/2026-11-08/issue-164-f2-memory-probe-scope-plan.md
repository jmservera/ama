---
title: Issue 164 F2 plan (memory probe scope reporting)
description: Prospective plan for a narrow offline report traceability correction, written before critique and implementation
ms.date: 2026-11-08
---

## Scope

Edit `src/agents/src/zava_forward/agents/chat_eval.py`, its existing `src/agents/tests/test_chat_eval.py`, and the chat-evaluation paragraph of `src/agents/README.md`. Add dated tracking evidence. Excluded: Core, API, `ChatPanel`, golden data, `chat_heldout.py` behavior, thresholds, prices, labels, registry, approvals, model or provider calls, Azure, KB index and log (no durable knowledge-base page changes), push, PR, merge.

## Phases

* [x] Phase 1: Research written ([research](../../research/2026-11-08/issue-164-f2-memory-probe-scope-research.md)).
* [x] Phase 2: Plan, details and one independent prospective critique ([critique](../../challenges/2026-11-08/issue-164-f2-memory-probe-scope-critique.md)), recorded before implementation; CR-001 to CR-003 accepted into the details.
* [x] Phase 3: Implement the report fields, README paragraph and focused tests; record changes ([changes](../../changes/2026-11-08/issue-164-f2-memory-probe-scope-changes.md)).
* [x] Phase 4: Focused validation, one Review ([review](../../reviews/2026-11-08/issue-164-f2-memory-probe-scope-review.md)), commit.

Details: [phase details](../../details/2026-11-08/issue-164-f2-memory-probe-scope-details.md).

## Constraints

* Existing pass/fail, enablement, gate and rate outcomes and all `bindings` stay identical; only descriptive fields are added, deterministically.
* The serving-path statement is derived from receipt `memory_used`, never asserted blindly.
* Focused CI-first tier only: `test_chat_eval`, `test_chat_heldout`, agents ruff and mypy in an isolated venv of this worktree. No FULL gate, SQL, browser or scanner. Hosted checks and independent exact-head assessment remain publication gates.
