---
title: Chat contact refusal gap fix and per-criterion status (issue 164)
description: Offline reproduction and fix of the send-style resident-contact ask that the live chat answered with a fallback instead of the refusal route, with the per-criterion proven/unproven table for the demo
ms.date: 2026-11-18
---

Refs #164. Scope is the synthetic demo, desktop only. This note follows the [third live pass](./issue-164-live-chat-grounding-evidence-r3-2026-11-18.md), which recorded that "Send the resident a text message now telling them the contractor arrives tomorrow." returned a fallback with no workflow route although the registry lists resident contact as refused.

## Finding

`out_of_scope()` in `src/core/src/zava_forward/core/chat_panel.py` matched only `send a letter/email/message/text` and `<verb> <resident>`. A send-style ask with the resident as indirect object ("Send the resident a text message", "Send the tenant an email", "Send an SMS to the resident", "Send the tenant a WhatsApp") fell through to the generic fallback. Reproduced offline before the change (six phrasings returned no refusal).

## Change

The `contact` pattern now also matches `sms` and `whatsapp`, `an` as article, and `send <resident|named person|them> a/an/the <channel>`. Added `test_send_style_contact_requests_are_refused_with_the_contact_route` and `test_questions_about_past_messages_are_not_refused` to `src/core/tests/test_chat_panel.py`.

## Validation (focused tier plus src checks)

* `src/core`: `unittest tests.test_chat_panel tests.test_regulatory_chat tests.test_exception_queue tests.test_usability_programme`: 123 tests OK.
* `src/agents`: `unittest tests.test_chat_eval tests.test_chat_heldout`: 76 tests OK.
* mypy in `src/core` and `src/agents`: no issues; `ruff check` and `ruff format --isolated --line-length 100 --check` clean on the changed files.
* Not run: `rpi-checks.py --all` (forbidden by the brief), the live re-probe. The live app runs the previously deployed image, and a redeploy is a production change outside this authority, so the fix is proven offline only.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Thresholds approved; task registered with accountable reviewer and enable state | Unproven (partly) | Registered and disabled (third pass). Thresholds proposed; accountable individual unknown. Person decision. |
| Results bound to serving-model and control versions with approved thresholds | Unproven | No actual-model chat result; nothing to bind. |
| Competent human exercises | Not needed for the demo | Owner decision 2026-11-18. |
| Actual calls need approved payload handling and finite authority | Unproven | No chat call authority granted; none made. |
| Out-of-scope refusal with route (ticked) | Proven offline, strengthened | New tests above; live gap fixed in source, undeployed. |
