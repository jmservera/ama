---
title: Issue 157 memory guard changes
ms.date: 2026-11-13
---

## Changes

* `controls.py`: `MEMORY_REF`, `is_memory_reference`, `evidence_text`, `MEMORY_REFUSAL` (single shared rule).
* `chatthreads.py`: chat message evidence uses the shared rule (adds `memory:` and `chat-memory`).
* `workflows.py`: six hazard evidence inputs plus hazard source and return/reopen source use `evidence_text`; `release_hazard` refuses stored memory-referenced prerequisite evidence.
* `change_provenance.py`: change and document source, version and reason refuse memory references.
* `quality.py`: checklist evidence and remediation notes refuse memory references; `evidence_gaps` and acceptance treat stored memory evidence as missing.
* Tests: `test_chat_memory.py` (references, prompt labels, gate and checklist), `test_hazard_referral.py` (hazard evidence and release).

## Validation

Targeted chat, gate and hazard tests, `ruff check`, `ruff format --check` and `mypy` in `/tmp/venv-157m-1819` pass. Full `src/core` unit discovery result recorded in the review step.

## Divergences

None from the revised plan. `gates.py` and `signoffs.py` are unchanged: they consume document kinds, and document provenance is now guarded at upload.
