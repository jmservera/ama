# Research: issue 164 remaining criteria (2026-11-01)

Disposition: executed. Planning Readiness: Ready.

* Issue #164 criteria 1, 2 and 5 are delivered by #307; #663 registered the disabled chat task and gates (Refs #164).
* Unmet and blocked by owner/live approval: approved thresholds and named accountable individual, held-out independent set, actual-model and human exercises, authorised spend, review-effort and cost.
* Deliverable offline: the known critical gap `grounding-unsupported-claim-with-valid-citation` (src/agents/evals/chat_golden.json). `parse_reply` in src/core/.../chat_panel.py accepts any claim whose citation id resolves.
* Option chosen: deterministic claim-level check in `ChatPanel` that withholds an answer asserting a status assurance word or a number absent from the cited source text. Conservative; offline; does not claim actual-model accuracy.
* Routed follow-up 1 (owner decision) and 3 (held-out set) remain open.
