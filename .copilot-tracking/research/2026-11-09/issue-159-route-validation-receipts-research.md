<!-- markdownlint-disable-file -->
---
title: Issue 159 route-level validation receipts research
description: Preparation research for the three authenticated HTTP 400 branches that bypass the chat panel receipt, with the #159 correction ledger
ms.date: 2026-11-09
---

## Disposition

* Research executed (focused, static reading only). Planning Readiness: Ready for the plan, NOT ready for implementation (parent not frozen, correction ledger not confirmed).
* Task slug: issue-159-route-validation-receipts. Mode: manual preparation. No source, test, gate, SQL, browser, model, remote or board action occurred.
* Source observations are static control-flow reading, not a runtime reproduction.

## Identities

* Worktree branch feat/demo-chat-validation-receipts-159-1109, HEAD d3810ffe489a6ceb048bfb35a14fca1f504bd1e7 (published #189 head, PR 1313, base main).
* Fetched origin/main 1464b4d850a89aaaf835ba8a9ad98d38aeb1fdd6. Merge base of the parent and main: 8d6f029cac004506953f36606862168bbe9d9412.
* Parent PR 1313 is open; hosted check `src-namespace` is FAILURE on the same head (owner brief: optional Azure import; native C4 fix running). The parent is RED and unfrozen.
* Between this HEAD and origin/main, the four chat files differ only in `server.py` by the #189 `simulator_admin` import and two route hooks. The `_chat` handler and `chat_panel.py` are identical, so the findings hold on both.

## Current handlers (src/api/src/zava_forward/api/server.py, `_chat`)

* Role gate (`projection.allowed`) runs before `_chat` and already records one access receipt for stored turn routes and for unstored-ask.
* `POST /api/chat/unstored-ask`: `set(body) - {"content","skill","case_id"}` raises `ValueError` BEFORE `c.current_user` and before `app.panel.ask_unstored`. Result: 400, no receipt. The later "Chat storage is approved" `ValueError` also skips a receipt but is outside the approved scope.
* `POST /api/chat/threads/{tid}/ask`: after `current_user` and `chat_resume` (denials already call `record_rejected`), extra keys beyond `{"content","skill"}` and an explicit `"skill": None` raise `ValueError` BEFORE `app.panel.ask`. Result: 400, no receipt.
* A non-null invalid skill on the stored route already reaches `ChatPanel._ask`, which raises inside `ask` and the `finally` audits one receipt (outcome `rejected`). Unstored invalid skill, empty or over-long content and a missing case already record via `_record_unstored_refusal` (#1085).

## Reusable receipt prior art (src/core/src/zava_forward/core/chat_panel.py)

* Stored: `ChatPanel._receipt(tid)` builds the full receipt (model_calls 0, tokens None, provider_outcome not-called, outcome `rejected`, cost Unknown with missing inputs, limits, memory_used False); `record_rejected` audits it as action `chat.turn` with outcome `access-rejected`.
* Unstored: `record_rejected_unstored` and `_record_unstored_refusal` audit action `chat.turn.unstored` with `{"outcome","model_calls":0}`; the question is never logged.
* Pattern: `with self.iso.store.lock: self.iso.store.audit(actor, action, target, json.dumps(detail, sort_keys=True))`. `actor` falls back to `unknown` when `user_key` raises.
* Audit seam: `Store.audit` (JSON file ledger) and `SqlStore.audit` (queued while a lock is held, committed at lock exit, otherwise `_audit_immediate`). New receipts reuse this seam unchanged; no schema, migration or new persistence.
* Sensitive-data note: `_record_unstored_refusal` stores the body-supplied `case_id` as the audit target before validation. The new branches have no validated case, so the plan records an empty target.

## Existing tests (prior art, unchanged)

* src/api/tests/test_chat_panel.py: `test_invalid_skills_do_not_store_or_infer` (asserts 400 for `skill: None` and others, no receipt delta), `test_unstored_ask_rejections` (extra key 400, no receipt delta), and receipt-delta plus canary patterns in `test_turn_refused_before_dispatch_still_records_a_receipt`, `test_foreign_and_missing_thread_turns_record_one_receipt_per_route`, `test_role_gate_denials_record_one_receipt_per_turn_route`, `test_unstored_ask_role_gate_refusal_records_one_receipt_without_the_question`, `test_regulatory_capability_refusal_records_one_receipt_per_turn_route`. Canary is `SECRET-QUESTION` with `assertNotIn` on the audit `detail`.
* src/core/tests/test_chat_panel.py: unstored rejection receipts (rows around lines 515 to 530) and an SQL-backed class with revocation receipts (around line 725), which are the persistence-seam controls.

## Correction ledger (existing #159 receipt lineage)

Sources: issue #159 comments (6, read in full on 2026-11-09), the eight `issue-159-*` and `chat-panel-*` state records under `.copilot-tracking/rpi-sessions/`, and PR metadata for 305, 307, 661, 840, 927, 1003, 1085, 1273.

| Item | Evidence | Ledger effect |
| --- | --- | --- |
| Issue comments | No comment grants, counts or exhausts correction cycles. The 7 Nov comment (6711077218) approves the bounded slice and requires FULL validation plus separate nonqueued admission. | No numeric grant exists on the issue. |
| RPI states | Seven completed loops, 2026-10-15 to 2026-11-04, each with one critique and one self-review "not independent". None records a correction-cycle count. | They are feature increments, not recorded correction cycles. Preserved as original history. |
| PR 661 | Copilot reviews at 05:18, 06:49 and 07:37 on 2026-11-01; one follow-up commit `test(api): cover rejected chat turn receipts on both routes` at 07:21; last review (verbatim thread target logging) came after it. | One evidenced review-correction commit. |
| PR 927 | Copilot "Changes recommended" at 19:12 (fallback wording), later commit at 20:23 on 2026-11-03; only one commit remains listed. | One possible correction, not provable from commit history. |
| PR 840, 1003, 1085 | One review or none; no post-review correction commit. #1085 merged as 075060f with four main merges only. | None. |
| PR 1273 (a5295c4) | Delivered the #530 actual SQL and employee-browser evidence; its own cycles belong to the #530 ledger. Refs #530, not #159. | Not a #159 correction; excluded from the count. |
| 2026-11-09 default | Owner-confirmed at most five total scoped correction cycles per issue, no reset, further cycles need issue-specific authorization. | Postdates all #159 PRs; retroactive application not stated. |

Conclusion: evidenced spent count is 1 (PR 661), possibly 2 (PR 927); the true number is not recorded anywhere. A new slug does not reset or add to it, and the remaining slice is an initial feature implementation, not a correction cycle. Upper-bound remaining corrections after this slice: three if two were spent and the five-cycle default applies retroactively. No new correction cycle is approved by this research.

## Adjacent unreceipted 400s (observed, NOT in the approved scope)

* Unstored route "Chat storage is approved. Use a chat thread." and non-object body 400s.
* Stored `messages` or `ask` on a regulatory thread raising "Use the bounded regulatory endpoint" before the panel.
* The legacy `messages` route ignores extra keys (no 400).
* Anonymous 401 and no-actor policy: explicitly excluded.

## Unmet criteria and boundaries

* #159 criterion 6 (named screen-reader and announcement acceptance) and the literal every-turn tokenomics criterion stay unmet; this slice would advance, not prove, the latter. Cost stays Unknown (OD-51).
* Demo-targeted validation tier applies (owner 2026-11-09). The 7 Nov FULL-validation wording and the repository security-sensitive full-tier rule conflict with it; the coordinator note records the owner replacement for this demo push and flags it for the review input.

## Blockers

* B1: parent PR 1313 is RED and not frozen; no code against it.
* B2: no confirmed #159 correction ledger or issue-specific authority.
* B3: nonqueued resource admission and independent exact-head review are not obtained.
