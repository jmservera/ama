# Changes: Epic #104 criteria 3 and 5 invariant suite

Plan: `.copilot-tracking/plans/2026-11-13/epic104-ai-nonmutation-limits-plan.md`.

## Added

* `src/agents/tests/test_epic104_bounded_ai_invariants.py` (22 tests, offline, stdlib `unittest`):
  * registry guard: exactly 13 capabilities, all unapproved, none live without the exact demo switch and profile, chat and concern pack disabled;
  * five assistants through `AgentWorker`: valid cited output is one unapproved proposal with an unchanged snapshot; approval, rank, transition and uncited outputs are rejected; the worker and chat adapters import no store module;
  * ranking: a biased AI proposal stays `Proposed`, differs from the deterministic order, cannot be resolved by another user, and leaves ranking and cases unchanged;
  * chat: golden run never enables; `ChatModel` refuses without admission before any call;
  * aftercare pack: unreviewed, owner-only review, concern record unchanged;
  * NFR-012 for every registered capability: no authority, expired authority, depth, token, call and money limits and unmeasured usage hold dispatch on the workflow-only route with an alert naming the authorised owner; a synthetic price holds a live call; `authorize` and `assistants.Limits` refuse unbounded settings;
  * held-out: a live batch runs only inside a complete authorisation and each missing limit refuses with no provider call; chat-eval `call_authorization` blocks each missing field.

## Not changed

* No production code, `infra/`, or #146-owned file. No bypass of the ledger or human-review routes was found outside those files.

## Validation (Focused tier, pip venv, not uv)

* `src/agents`: unittest discover with `PYTHONPATH=../core/tests`: 470 tests OK; `ruff check .` and `ruff format --check` clean; `mypy` clean (55 files).
* `src/core`: aftercare, ai_consumption, assistants_identity, chat_panel, priority_order, rai_release, ranking and regulatory_usage modules: 522 tests OK (82 skipped for optional prerequisites).
* Hosted CI was not run (nothing pushed). The complete local gate was not run: Focused tier, tests-only change.
