# Plan: chat origin badge accessibility tests (#215, #164)

Date: 2026-11-14. Research: `.copilot-tracking/research/2026-11-14-chat-origin-badge-a11y-research.md`.

* [x] Add `src/api/tests/test_chat_origin_badge_a11y.py` (new file only; no `checks/*`, no source edits).
  * Pin distinct origin labels for rule, generative and withheld replies.
  * Pin detail text, rule tags and per-outcome live status text.
  * Pin polite live regions, message text order, text-based outcome and `Sources (N)` disclosure with empty-source note.
  * Guard origin copy against internal jargon.
* [x] Validate: targeted unittest trio plus `ruff check` and `ruff format --check`.

Critique: executed once inline; verdict compatible, no conflicts. Tier: focused (test-only addition). Hosted CI not observed; branch not pushed.
