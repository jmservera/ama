---
title: Issue 157 memory guard review
ms.date: 2026-11-13
---

## Review

Executed once (code-review agent) after implementation. Outcome: two Medium findings, both fixed in the working tree before commit.

* Hazard handoff evidence in `challenges.py` was unguarded: fixed with `controls.is_memory_reference` and a test.
* The `CM-` pattern rejected legitimate references such as `CM-2024`: narrowed to the generated id shape (`CM-` plus 12 or more hex digits), `memory:` now requires a following non-space character; negative tests added.

## Validation

* `ruff check`, `ruff format --check` and `mypy` in `src/core`: pass.
* 449 targeted tests (chat, memory, gates, hazard, challenges, quality, provenance, finance sign-offs): pass, 1 skipped.
* Full `src/core` unit discovery exceeded the session time limit twice and was not completed; this is not claimed as run.
