---
title: Resident chat learning record and router research
ms.date: 2026-11-01
---

* Research disposition: executed. Planning Readiness: Ready. Refs #466; #163 deferred.
* Findings: `chat.route()` in `src/api/src/zava_forward/api/resident_demo/chat.py` is a whole-sentence regex router. "Can I unpause it?", "How do I unlock my case? Who should I contact?" and "What docs are missing?" matched no pattern, and any `contact` word returned the refusal. "Why is my case blocked?" routed to status, whose recorded text is only "Contact is paused."
* Recorded facts available: `view["progress"]` and `next_step` from the stage text (`resident_preview.STAGE_TEXT["Contact paused"]`) and the housing officer route in `HUMAN_HELP`. No phone numbers, names or addresses are recorded.
* Store pattern: `agenda.py` keeps a local SQLite file selected by `ZF_DEMO_AGENDA_PATH`. The session cookie carries a random per-sign-in id (`SessionCodec.verify` returns it), which is not the resident identity.
* Constraints: existing tests pin refusals, so route() keeps returning "unknown" and the refused versus unrouted split is a separate classification. Consent box text is unchanged; the visible copy avoids gate, hold, provenance, trace, snapshot and envelope.
* Decisions: SQLite file via `ZF_DEMO_CHAT_LOG_PATH` (optional, no new infrastructure); 14-day and 2,000-row caps; 200-character question with masking; CLI summary for operators.
