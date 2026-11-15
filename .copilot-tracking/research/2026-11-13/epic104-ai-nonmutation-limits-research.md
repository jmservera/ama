# Epic #104 criteria 3 and 5: AI non-mutation and NFR-012 limits research

Task: `epic104-ai-nonmutation-limits` (state: `.copilot-tracking/rpi-sessions/2026-11-13/epic104-ai-nonmutation-limits-state.json`).
Branch `test/demo-104-ai-nonmutation-limits-2244`, base `9c8c89890ce783cf78761af0698e42c928dbca2f`, target `main`.
Research disposition: executed. Planning Readiness: Ready.

## Scope

Issue #104 (read with `gh issue view 104 --comments`, 2026-11-13), two unticked criteria:

* Criterion 3: AI never approves, executes, ranks or mutates controlled records.
* Criterion 5 (tokenomics delta): no registered AI capability is enabled beyond the exercise without finite, owner-approved call, token and budget limits and an owned alert (BRD NFR-012).

Non-overlap (owner brief): an active #146 worker owns `infra/`, `ai_consumption.py`, `monitoring_coverage.py`, `agents/.../worker.py` and `api/.../server.py`. This task writes only a cross-capability test suite under `src/agents/tests/` and, if a real bypass exists outside those files, a minimal isolated fix in `src/agents/`.

## Read manifest

* `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md` (searched for AI bounds), `docs/reference/README.md` index, `docs/reference/memory.md` (context only, not evidence).
* BRD `docs/brds/agentic-retrofit-programme-brd.md` NFR-012 (line 1603) and OD-51 (line 2169). NFR-012 AC-100: each capability and period has a finite owner-approved call, token and budget limit with an alert threshold and a named alert owner; reaching a limit degrades to the workflow-only path.
* Source: `core/ai_registry.py`, `core/assistants.py` (`REGISTRY`, `Limits`, `disabled`, `shape_result`, `validate_output`, `review`), `core/ai.py` (`Ai._request`, `is_live`), `core/ai_consumption.py` (`authorize`, `reserve_in`), `core/ai_consumption_demo.py` (`DemoPort`), `core/chat_panel.py`, `core/store.py` (`ai_priority`, `resolve_priority`), `core/ranking.py`, `core/aftercare.py` (`propose_pack`, `review_pack`), `agents/dispatch.py`, `agents/chat.py`, `agents/chat_eval.py`, `agents/chat_heldout.py`, `agents/heldout_batch.py`, `agents/ai_eval.py`, `agents/cohort_ai_eval.py`.
* Not read: Azure infrastructure, #146 files beyond the read-only inspection above.

## Findings

Registered capabilities (`ai_registry.tasks()`): the five assistants (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`), six retained paths (`briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`), `chat-case-conversation` and `aftercare-concern-pack`. Every entry is `unapproved`, has `UNKNOWN` authorities and states "no write, send, approve or rank".

Criterion 3 mechanisms already present:

* Worker (`dispatch.AgentWorker`) has no store; `shape_result` forces `approved=False`; `validate_output` closes the output to `summary`, `findings`, `unknowns` with captured citations.
* Human review route (`Assistants.review`) needs verify, then accept or edit-accept by a named human; `Store.resolve_priority` accepts only the recommendation's owner; the AI recommendation stays `Proposed` beside the deterministic order (`rec["deterministic"]`).
* Chat panel refuses approve, decide, consent, contact and diagnose asks before any model call; `ACTION_CLAIM` withholds model claims of approval.
* Aftercare concern pack is template-first, `approved=False`, reviewed only by the named owner, changes nothing on the concern.

Criterion 5 mechanisms already present:

* Assistants: `Limits` is invalid (work refused) without authority, finite calls and tokens, and an expiry; `disabled()` also checks release admission, shared allowance and expiry.
* All model calls: `Ai._request` reserves in the consumption ledger first. `reserve_in` holds with an alert event (owner, route `workflow-only`) for no authority, expired authority, no price, synthetic price on a live call, unknown liability, depth, call, token and money budget limits. `authorize` rejects non-finite limits, zero calls or depth, empty budgets and missing price.
* Chat: `authorizes_live` is false except the owner-approved demo switch with the demo profile; dispatch still needs the ledger.
* Held-out adapters: `chat_eval.call_authorization` and `heldout_batch.authorization_problems` need a named owner, finite calls, tokens, budget and expiry and stop before a breaching call.

Existing tests prove each mechanism per component. No single suite enumerates the registry and proves the invariants across all capabilities, so a newly registered capability or a weakened gate would not fail one place.

## Gap analysis and bypass search

* No bypass of criterion 3 found outside #146 files.
* No bypass of the ledger limits found: every `Ai` dispatch reserves first.
* Residual, not changed here: the held-out adapters' authorisations (`chat_eval.call_authorization`, `heldout_batch.authorization_problems`) carry a named approving owner and finite limits but no separate alert threshold or alert owner field; breach is reported with the approving owner and a stop reason. Adding a required field changes gate semantics and fixtures, so it is recorded as a ranked follow-up, not a silent change. Ledger capabilities do carry an alert owner (`authorize(owner=...)`; fallback `unassigned-owner-OD-51` holds dispatch).
* Criterion 5 stays unticked by this task: the evidence is local synthetic; OD-51 (owner approval of real budgets, alert owners, price source) is open and Azure/billing evidence is not produced.

## Selected approach

One new suite `src/agents/tests/test_epic104_bounded_ai_invariants.py`, hermetic, stdlib `unittest`, no network:

1. Registry guard: pinned capability set equals the registry; every entry unapproved, never live-authorised (only the exact demo switch plus profile honours chat); concern pack and chat disabled.
2. Five assistants through `AgentWorker`: hostile provider outputs (approval flags, rank, extra keys, uncited claims) are rejected or unapproved; snapshot unchanged; one provider call; worker modules import no store or controlled-record module.
3. Ranking immutability and human route with a real `Store`: scripted AI reorders, deterministic order and case records unchanged, recommendation `Proposed`, only the owner can resolve, accept leaves ranking unchanged.
4. Chat: panel refuses action asks with no model call and no state change; an unapproved admission denies `ChatModel`; chat_eval and held-out freeze never enable.
5. Concern pack: template-first, unapproved, only the owner reviews, concern record unchanged.
6. NFR-012: for every registered capability, no authority, expired authority, synthetic price on a live call, and each of call, token and money budget exhaustion hold dispatch with an owned alert and workflow-only route; `authorize` refuses non-finite, zero or missing limits; `Limits` refuses each missing or unbounded setting; held-out and chat-eval authorisations refuse each missing limit and make no call.

## Validation tier

Focused tier (owner brief). Tests-only, no workflow, gate-tool, dependency or Dockerfile edit, no infrastructure, deployment, SQL or security-control change. Hosted CI not read (nothing pushed); stated as not run.

## Planning Readiness

Ready.
