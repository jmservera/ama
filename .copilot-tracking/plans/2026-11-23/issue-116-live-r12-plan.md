# Plan 2026-11-23, issue 116 live r12

Tier FULL (src change, provider-boundary security control).

1. Add a failing test in `src/core/tests/test_ai_input_bounds.py`: several images each under the cap, total over it, refused with `input-image-too-large`; one image at the cap still passes.
2. Sum image bytes in `approved_payload` and refuse above `MAX_IMAGE_BYTES`.
3. Run core boundary suites and api consumers, ruff, mypy; write the research note, README index and log entries.
4. Review once, commit locally.
