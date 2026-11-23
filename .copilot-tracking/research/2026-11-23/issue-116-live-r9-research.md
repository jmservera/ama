# Research 2026-11-23, issue 116 live r9

Disposition: executed. Planning readiness: Ready.

One unticked box: allowlists at every provider boundary. Skipped owner-only items.

Finding: `core/ai.py` `approved_payload` returns early for a string `user`, so the shared type and size allowlist does not bound it. The size limit for string input runs later in `_request_body`, after the simulation verifier and the data-protection hold, so those gates see an oversized prompt first and a hold can mask the refusal. Existing tests (`test_ai_input_bounds`) pass because the later check still fires.

Proposed fix: count string `user` bytes in `approved_payload`, so every provider family (run, _chat, evidence, look_at) refuses before any other gate. Test: oversized string refused with `input-too-large` even when a data-protection hold is set and the verifier is absent.
