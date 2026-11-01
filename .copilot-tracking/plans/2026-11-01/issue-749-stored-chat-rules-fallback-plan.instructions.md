# Plan: issue 749 stored chat rules fallback

Recorded after implementation (2026-11-01); the work was done first and this plan documents what was executed. No critique was run before implementation; the independent review is [issue-749-review.md](../../reviews/2026-11-01/issue-749-review.md).

Tier: focused. Details: [issue-749-stored-chat-rules-fallback-details.md](../../details/2026-11-01/issue-749-stored-chat-rules-fallback-details.md)

* [x] Phase 1: in `ChatPanel._ask`, when a case thread's reply would be `FALLBACK`, return the rules-based grounded answer with case-fact citations and a rules-only note.
* [x] Phase 2: add `StoredRulesFallbackTests` and update tests that asserted the old fallback.
* [ ] Phase 3 (owner): verify on a live redeploy that stored case chat is grounded with AI off.
