# Details 2026-11-23, issue 116 live r9

Phase 1: replace the `if isinstance(user, str): return` early exit in `approved_payload` with a byte count that falls through to the shared size check. Keep the structured-list branch unchanged. Tier FULL (src change); no rpi-checks --all here.
