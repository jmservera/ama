---
title: Issue 157 memory never evidence guard plan
ms.date: 2026-11-13
---

## Plan

* [ ] Phase 1: add `controls.is_memory_reference` / `controls.evidence_text` (single shared rule for `CM-`, `memory:`, `chat-memory`); reuse in `chatthreads._clean_evidence`; use `evidence_text` for the six hazard evidence inputs in `workflows.py`.
* [ ] Phase 2: tests in `test_chat_memory.py` (all reference forms rejected for chat evidence; `build_prompt` memory block carries `authority none`, `evidence false`) and `test_hazard_referral.py` (memory refs refused as hazard decision evidence; gate and sign-off checklists cannot be satisfied by memory).
* [ ] Phase 3: run chat, gate and hazard tests, ruff check, ruff format --check, mypy in `/tmp/venv-157m-1819`; independent review; commit locally.

Details: [details](../../details/2026-11-13/157-memory-never-evidence-guard-1819-details.md)

## Critique disposition (rubber-duck, one pass, all applied directly)

* Also guard `raise_hazard` source, `_disposition` source, `change_provenance` source (document provenance), quality checklist items and remediation note.
* Gates read stored evidence: `quality.evidence_gaps` treats memory-referenced item evidence as missing; `accept_quality` treats memory remediation evidence as missing; `release_hazard` rejects stored memory-referenced prerequisite evidence.
* Narrower grammar: alphanumeric-boundary `CM-` plus 4+ hex digits, `memory:`, `chat-memory` not followed by `-`, word character or dot; negative tests for `5 cm-thick insulation` and `chat-memory-dpia.md`. Chat message evidence keeps the stricter existing `CM-` prefix rule.
* `document kind` assumption corrected: a document's source is guarded at upload so memory-sourced documents cannot be created; a test pins this.
