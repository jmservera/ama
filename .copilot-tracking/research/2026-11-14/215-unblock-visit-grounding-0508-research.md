# Research: #215 unblock and visit grounding (Refs #215)

Disposition: executed (local source inspection only; no cloud, Docker or full gate).
Base: 40266b643 on test/demo-215-unblock-visit-grounding-0508, stacked on PR #1630.
Planning Readiness: Ready.

## Owner failure mode

Safety-stopped case, three turns: "what can I do to unblock this case?", "review what is blocking it", "how can we fix this safety? Should we schedule a visit?".

## Findings (current source)

* Routing: `src/core/.../chat_case_answers.py` `INTENTS` maps turns 1 and 3 to `unblock` (patterns `unblock`, `fix ... safety`, `should we schedule`) and turn 2 to `blocked`. `answer()` returns cited deterministic text; `_unblock` states "A person schedules visits and completes the safety step ... This chat cannot book a visit or approve a safety step.", lists open hazards, then the cited blockers.
* API path: `src/api/.../server.py` `_chat` routes `threads/{id}/ask` and `unstored-ask` to `ChatPanel` (`chat_panel.py`). `out_of_scope` refuses action requests; the three questions are not refused (existing test `src/api/tests/test_chat_panel.py::test_blocked_case_questions_are_answered_with_cited_sources`, PR #1576).
* Provenance: `ChatPanel._reply` sets `answer_source` to `decision-rules` (workflow-only), `generative-grounded`, or `decision-rules-fallback` (generative draft failed the unsupported-claims check or abstained, replaced by cited rules plus FALLBACK_NOTE). `SOURCE_LABELS` carries the server copy; `chat.js` `attribution()` renders "Decision model (...)" versus "Model-generated, not approved. Demo only." and the entry warning "Chat cannot approve or change records."
* Gates: `parse_reply`, `unsupported_claims`, citation permission check, withheld and ungrounded kinds; citations carry `source_kind` (`decision-rule` or `case-record`).
* Reproduction: no deterministic grounding or provenance defect reproduced. The new tests pass on current source.

## Gaps noted, not changed

* The deterministic unblock text names human scheduling and that chat cannot book or approve, and cites the hazard owner (for example Safety lead) from the record, but states no resident-consent step. That is new product copy needing owner and resident-engagement review, outside the "genuine bug" fix condition. Routed as a follow-up.
* The installed `zava_forward` in the shared environment points to another checkout; tests ran with PYTHONPATH set to this worktree's `src/*/src`.
