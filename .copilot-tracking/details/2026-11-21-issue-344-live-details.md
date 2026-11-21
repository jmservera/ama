# Details: issue 344 live (2026-11-21)

Phase 2: in `src/core/src/zava_forward/core/workflows.py` `unaccepted_handoffs`, wrap `handoff_ageing` in `try/except (KeyError, ValueError)` and `continue`. The as-of and limit validation stay before the loop, so caller errors still raise. `handoff_ageing` is unchanged (existing test expects KeyError for a missing offered_at).
Phase 3: test offers two handoffs, ages one with a valid offset time and one with naive "2026-10-15T10:00"; asserts the call returns only the valid case.
