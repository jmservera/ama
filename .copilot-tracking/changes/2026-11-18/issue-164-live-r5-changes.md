# Issue 164 r5 changes
Tier: FULL class (src changed); `rpi-checks.py --all` not run per brief; focused checks recorded. Note: the earlier r4 artifacts are preserved; this pass uses r5 names. Witness events seq 1-4 reference the first-created r4-named paths, renamed to r5 before any commit.

Files: `src/core/src/zava_forward/core/chat_panel.py` (contact pattern), `src/core/tests/test_chat_panel.py` (2 tests), `docs/reference/research/issue-164-contact-refusal-gap-2026-11-18.md`, index, log.

Validation: core 123 tests OK; agents chat_eval and chat_heldout 76 OK; mypy core and agents clean; ruff check and format clean.

| Criterion | Proven? |
| --- | --- |
| Thresholds approved; accountable reviewer; enable state | Unproven (person decision) |
| Bind to serving-model versions with approved thresholds | Unproven (no actual-model result) |
| Human exercises | Not needed for demo |
| Actual calls need finite authority | Unproven (none granted) |
| Contact refusal with route (ticked) | Gap fixed offline; live undeployed |
