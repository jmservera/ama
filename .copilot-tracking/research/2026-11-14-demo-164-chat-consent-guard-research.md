# Research: #164 officer chat consent boundary (2026-11-14)

Disposition: executed. Planning readiness: Ready. Refs #164, Refs #215.

* Path correction: `src/api/src/zava_forward/api/chat.py` does not exist. Officer chat logic is `src/core/src/zava_forward/core/chat_panel.py` (`ChatPanel._ask`, `ask_unstored`), rules text in `chat_case_answers.py`, scope/projection in `chat_isolation.py`, rendering in `src/api/src/zava_forward/api/web/chat.js`. `tests.test_chat` does not exist; the nearest suite is `tests.test_chat_panel`.
* chat.js already renders `answer_source=decision-rules` as "Deterministic decision or workflow rule (not generative AI; no record changed)" and tags `workflow/` citations `[Workflow rule]`. No JS change needed.
* Gap: no case-level resident AI/data-use consent state exists (only per-home sensor consent and the resident decision status). A consent-missing case still reaches the model path. Seed cases carry no such field.
* Decision: an explicit `resident.ai_data_use_consent` state other than `Given` (Not requested, Pending, Declined, Withdrawn, or an empty value) blocks model calls. An absent field is legacy and unchanged, so existing behaviour is preserved. Open owner decision: whether absent should also block once the field is captured for all cases.
* Not evidenced: live model, rendered browser, screen reader, staff comprehension.

## Cycle 1 correction

Research: review finding is a single E501 line in chat_panel.py:360; no scope change. Refs #164.
