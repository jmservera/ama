# Details: 891 chat grounding core (revised after critique)

## Design

* permitted_sources: walk keys in PRIORITY order (id, stage, status, owner, waiting_on, reason, work, gate, hazards, funding, funding_ok, checklist, technical_missing, documents, appointments, decision, resident) then remaining sorted keys. MAX_SOURCES stays 60: 90 sources of up to 200 chars would exceed MAX_INPUT_CHARS and trip LIMIT_REACHED.
* INTENTS: new `unblock` intent placed FIRST (so "how do I unblock funding" gets blockers): unblock\w*, how can/do/to I/we fix/resolve/clear/unblock, safe\w*, safety, visit, schedul\w*. Answer: human-action disclaimer first (no cites, so truncation cannot drop it), recorded active hazard lines, then `_blocked`.
* _ask fallback: only when a model call was made; facts filtered through the selected skill scope via skill_sources; citations and sources come from the exact rules facts used; only when grounded_answer returns "answer" with cites; only for abstain or withheld with text == UNGROUNDED. Source `decision-rules-fallback`, model `workflow-only`, receipt model_calls kept.
* _reply gains answer_source, answer_source_label, citation source_kind; finish() only passes the override when final kind is "answer" (settlement downgrade resets it to kind).
* ModelUnavailable(meter_id, meter_root) copied into receipt on catch; test with a raised exception and mocked publish_output.
* SYSTEM: `*` bullets, no numbered lists, no status words unless literally cited, exact ids.

## Known limit

Recorded values are interpolated as written; banned-word filtering of case data is out of scope (rules wording is clean).
Write surface strictly: two sources and two tests.
