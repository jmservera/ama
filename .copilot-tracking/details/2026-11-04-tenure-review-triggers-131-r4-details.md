# Details: tenure review triggers (R4)

* Phase 1: append-only `review_triggers` on a report (Changed scope, Dispute, Defect, Charge query, Ambiguous lease identity) with source, named owner, next update and routing text. Open triggers make `_pack_is_current` false and refuse Verified and pack drafts. Ambiguous identity sets `reuse_blocked`, Unknown verification and route. Resolution needs a named other person; data owner role for ambiguous identity.
* Phase 2: core tests (each of four triggers, ambiguous identity, unsafe input); API test (403 restricted role, hidden from restricted projections).
* Phase 3: core and API README contract; log.md entry.
