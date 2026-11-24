# Issue 116 live r14 research (2026-11-24)

Disposition: executed. Planning Readiness: Ready.
Only unticked box: allowlists at every provider boundary. Four HTTP boundaries exist: core Ai (ai.py, uses approved_payload), resident_demo assistant.py (512-byte ascii prompt bound), resident_demo aoai.py (500-char question), agents heldout_aoai.py (no input allowlist: system and prompt sent as is). Gap: heldout_aoai.
Live: payload contents are not observable from deployed apps; credentials not needed.
