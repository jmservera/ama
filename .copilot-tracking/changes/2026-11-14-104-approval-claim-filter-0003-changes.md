---
title: Issue 104 approval claim filter changes
ms.date: 2026-11-14
---

## Changes

* Modified `src/core/src/zava_forward/core/ai.py`: tightened `FORBIDDEN`.
* Added `src/agents/tests/test_ai_claim_filter.py` and `src/api/tests/test_assistant_reserve_guard.py`.

## Validation

* ruff check (E,F,I,B,UP, 100) and format on new files: pass. `ai.py` was already unformatted before this change; not reformatted to avoid unrelated churn.
* mypy: core pass; agents pass; api reports pre-existing playwright import errors only, none in new files.
* agents unittest discover: 51 pass. core scenario manifest, assistant drafting and ai_consumption: pass. api `test_ai_consumption_api` 40 pass plus new guard test.
* Full api discover was not completed (stalled over 20 minutes), so only targeted api tests ran.
* No hosted CI observed; nothing pushed.

## Divergence

Filter lives in `src/core` (where `Ai.run` is defined), with tests in agents and api as requested.
