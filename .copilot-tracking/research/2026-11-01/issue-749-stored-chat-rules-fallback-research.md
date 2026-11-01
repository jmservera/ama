# Research: issue 749 stored chat rules fallback

Recorded after implementation (2026-11-01). It summarises what the implementation commit 1ab45d61f and its review evidence established; no separate research phase preceded the fix.

## Problem (issue #749)

* Live Playwright checks on 2026-11-01 against the redeployed demo (main 398e846fd, revision 0000008) showed that with chat storage approved and AI unavailable, case chat replied with the generic "assistant not available" text, Skill general and Sources (0).
* Issue hypothesis: the rules-based case grounding added in #743 ran only in the unstored path; `web/chat.js` routes stored chats to `/api/chat/threads/{id}/ask`.

## Findings (from code inspection during the fix)

* `ChatPanel._ask` in `src/core/src/zava_forward/core/chat_panel.py` returned `FALLBACK` when the model was absent or failed.
* The rules answer (`grounded_answer`) was wired only in `ask_unstored`.
* Existing tests asserted the old generic fallback, and the chat eval golden run asserted zero non-AI panel answers.

## Planning readiness

Ready: reuse `grounded_answer` and `iso.case_facts` in the stored path; keep refusals, limit-reached and withheld paths unchanged.

## Evidence

* Issue #749; review: [issue-749-review.md](../../reviews/2026-11-01/issue-749-review.md)
* Live evidence referenced by the issue: `.copilot-tracking/redeploy-chat-2026-11-01/`
