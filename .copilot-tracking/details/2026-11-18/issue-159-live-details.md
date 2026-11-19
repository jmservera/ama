# Issue 159 live details

Phase 1: sign in with `login.py` (credentials read at runtime, not printed), open case ZF-2025-0122, press Tab until the launcher is focused, Enter, observe focus, tab order, log/status attributes, two typed turns sent with Enter, MutationObserver records, Escape focus return.

Phase 2: `shots-keyboard.py` crops launcher, header and composer; run `test_assistant_panel_a11y_159.py`; `cleanup-own-threads.py 40` deletes only threads on the probe case younger than 40 minutes; remove `<tmp>/state-staff.json`.

Phase 3: write `docs/reference/research/assistant-ux-live-159-2026-11-18.md`, add an index row and log entry, commit with `Refs #159`. No source edits; FOCUSED tier (documentation, scripts and evidence only).
