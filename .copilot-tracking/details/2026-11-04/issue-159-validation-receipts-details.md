<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refused receipts details
description: Phase details for the validation-refused receipt slice
ms.date: 2026-11-04
---

## Phase 1

* File: src/core/src/zava_forward/core/chat_panel.py. Wrap skill, question-length, empty-question and case-facts checks in `ask_unstored`; on ValueError, PermissionError or LookupError write one audit row (`chat.turn.unstored`, outcome, `model_calls` 0) then re-raise. Question text is never written.

## Phase 2

* File: src/core/tests/test_chat_panel.py, `test_unstored_validation_and_missing_case_refusals_record_receipts` (four refusal kinds, exactly one receipt each, no question text).
