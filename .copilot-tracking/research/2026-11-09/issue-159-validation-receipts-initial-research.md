<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refusal receipts, initial implementation research
description: Re-research of the exact qualified #189 parent for the three authenticated HTTP 400 chat branches that bypass the panel receipt
ms.date: 2026-11-09
---

## Disposition

* Research executed (new, against the qualified parent), superseding the PREPARATION research as the base for the plan. The earlier file `issue-159-route-validation-receipts-research.md` is preserved unchanged as history, including its correction ledger.
* Task slug: issue-159-validation-receipts-initial. Refs #159, Refs #189. Planning Readiness: Ready.
* Exact base read: parent `e192bc74732e824a3488c49a4875df9bd4463cd8` (local branch `feat/demo-simulator-control-189-1109`, coordinator-qualified clean), read with `git show` before any merge. Candidate base `b851a9e2c793246494085c34a906845a97603b7d`. Fetched `origin/main` `2b6d80a2580444751d4b85fc8eaa2c15f367855d` is NOT an ancestor of the parent (merge base `3a9767d5c`); the parent declared stack is the target, not main.
* Authority: coordinator disposition 2026-11-09 (new initial feature increment; consumes no correction cycle; no new cycle granted). Historic count preserved: 1 confirmed, 1 possible, true total unrecorded.
* Tier: owner-selected demo-targeted (modified plus impacted modules, pinned Ruff 0.17.1, API and Core strict mypy 2.4.0). No full gate, Docker, SQL or browser by default.

## Current handler (parent e192bc74, `src/api/src/zava_forward/api/server.py`, `_chat`)

* Role gate at the `/api/chat` dispatch precedes `_chat`; `_chat` maps `ChatNotFound`/`LookupError` to 404, `ChatForbidden`/`PermissionError` to 403 and `ValueError`/`TypeError` to 400.
* Branch A, unstored: `post and parts == ["unstored-ask"]` raises `ValueError("Only content, skill and case_id are accepted.")` on any extra key BEFORE `c.current_user` and before `app.panel.ask_unstored`. No receipt.
* Branch B, stored extra keys: `parts[2] == "ask"` raises `ValueError("Only content and skill are accepted.")` after `chat_resume` succeeded (thread owned and permitted) and before `app.panel.ask`. No receipt.
* Branch C, stored explicit `skill: null`: raises `ValueError("Choose a listed skill or omit skill for legacy chat.")` at the same point. No receipt.
* Invalid listed-skill values already reach `ChatPanel.ask`, whose `finally` writes a `chat.turn` receipt with outcome `rejected`; `ask_unstored` writes `chat.turn.unstored` `{outcome: rejected, model_calls: 0}` through `_record_unstored_refusal`. The three branches are the only chat-turn validation 400s that skip the panel.
* The #189 parent adds only simulator-admin routes to `server.py`; `_chat` and `chat_panel.py` are byte-identical to the candidate base (`git diff b851a9e2 e192bc74 -- src/core/src/zava_forward/core/chat_panel.py` is empty). `store.py` differs only by unrelated quality-evidence gate lines; the `audit` seam is unchanged.

## Reusable prior art (`src/core/src/zava_forward/core/chat_panel.py`)

* `ChatPanel._receipt(tid)`: fixed metadata only (`thread_id`, `task`, `model_calls=0`, `tokens=None`, `provider_outcome="not-called"`, `outcome="rejected"`, `cost="Unknown"`, `missing_cost_inputs`, limits, `memory_used=False`). Token semantics stay UNKNOWN (`None`).
* `record_rejected(user, tid)` and `record_rejected_unstored(user)` write one audit entry under `store.lock` through `Store.audit` / `SqlStore.audit`. No new audit seam, action name or schema is needed.
* Stored receipts keep the audit target empty; unstored refusals use `chat.turn.unstored` with `{outcome, model_calls}` only.

## Findings that shape the plan

* One helper in core, narrowly named `ChatPanel.record_validation_refused(user, tid=None)`: stored when `tid` is given, unstored otherwise. Outcome is the existing vocabulary `rejected`, matching the invalid-skill receipt, so no new outcome strings.
* The helper receives no body content, so the question, unknown field names and values and any raw skill cannot reach the receipt or audit by construction. The unstored target is empty (the body `case_id` is unvalidated). The stored `tid` is retained only after `chat_resume` proved it is the caller's permitted thread.
* Permission: the helper rechecks with `iso.current_user`. If the user is no longer permitted, it writes nothing and returns, so the existing 400 is preserved and no duplicate or new denial receipt is created (anonymous and no-actor policy are out of scope). This replaces the earlier D1 (400 to 403) default, which would have changed an HTTP status the brief says to preserve.
* Duplicate-receipt risk: both stored raises precede `ChatPanel.ask` (the only other `chat.turn` writer for ask) and the unstored raise precedes `ask_unstored`. Exactly one receipt is therefore structural.
* Audit lock: the helper owns its own `with store.lock` block and returns before the handler raises, the same pattern as `record_rejected`. A write failure would surface as a 500 as it does for the existing rejected receipts; this is an accepted existing-seam property, not a new policy.
* No change to `store.py`, `sqlstore.py`, schema or migration. If implementation shows the audit seam must change, STOP and report scope expansion.

## Test seams (existing files only)

* `src/api/tests/test_chat_panel.py` (`PanelTests`, role-matrix HTTP harness) already counts receipts for denials (`test_foreign_and_missing_thread_turns_record_one_receipt_per_route`, `test_unstored_ask_role_gate_refusal_records_one_receipt_without_the_question`) and has `test_unstored_ask_rejections` and `test_invalid_skills_do_not_store_or_infer` for 400 and no-inference. These supply the helper functions for a model-call spy, audit reading and canary assertions.
* `src/core/tests/test_chat_panel.py` has `StoredQuestionTests` and `UnstoredAskTests` for panel-level receipts and the audit chain; the helper test belongs there.

## Not in scope (unchanged)

* Anonymous or no-actor 401 policy, other 400 branches (unstored "storage approved", regulatory-thread, non-object body, `messages` route), UI and assistive-technology acceptance, provider activation, real models, cloud, private data, whole-issue closure, named screen-reader acceptance and OD-51 cost. Human, manual, proposal-only and consent boundaries unchanged.

## Open questions

* None blocking. Independent exact-head review stays required before publication; hosted CI is the coordinator's to observe.
