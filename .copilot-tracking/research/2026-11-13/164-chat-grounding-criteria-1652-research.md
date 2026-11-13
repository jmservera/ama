# Research: issue #164 remaining acceptance criteria audit

Task: `164-chat-grounding-criteria-1652`. Date: 2026-11-13. Research disposition: executed. Planning Readiness: Ready.
Base: worktree HEAD `3ffb8c0e7`, an ancestor of `origin/main` `6f9bb5074`; `git diff HEAD origin/main` over `src/agents` and `ai_registry.py` is empty, so the audited code is current main. Tier: Focused (documentation-only audit; no executable change).

## Scope

Three unchecked criteria of #164 (4 of 7 ticked): memory poisoning and prompt-injection pass before enablement; thresholds approved and chat task registered with reviewer and enable/disable state; any actual evaluation call stays within a finite owner-authorised call, token, budget and expiry limit. Latest issue comment states independently labelled held-out data, actual serving-model adversarial evidence, approved thresholds and reviewer, competent-human exercises and finite real-call authority remain unproved, and that no remaining criterion is accepted.

## Evidence gathered

Tests run in `/tmp/venv-164-1652` (pip editable installs of `src/core`, `src/agents`, `src/api`), all passing:

| Command (from component dir) | Result |
| --- | --- |
| core `test_chat_*.py` (13 files incl. memory, privacy, panel) | 119 tests OK |
| api `test_chat_*.py`, `PYTHONPATH=../core/tests:../agents/tests` | 103 tests OK, 2 skipped |
| agents `test_chat_model.py` | 17 OK |
| agents `test_heldout_batch.py` | 40 OK |
| agents `test_chat_eval.py` (added: it holds the gate, registry and call-limit tests) | 45 OK |

Code findings in `src/agents/src/zava_forward/agents/chat_eval.py`:

* `GATE_CATEGORIES` include `prompt-injection` and `memory-poisoning`; results come from a scripted provider over a synthetic store (module docstring: says nothing about an actual model). `OPEN_ITEMS` states integrated memory poisoning is "not covered", the isolation memory assertions are component-only, refusal and action-claim checks are lexical and paraphrase-bypassable, and actual-model evaluation and the held-out set are not produced. `enablement_decision` always returns `state="disabled"` and `insufficient` unless a gate fails.
* `enablement_decision` lists `approved thresholds`, `accountable reviewer`, `independently labelled held-out set`, `actual-model evaluation`, `human exercises` as missing evidence; `actual_calls` is computed from `call_authorization(None, ...)`, which is `blocked`.
* `call_authorization` fails closed on missing named owner, non-finite or exhausted call/token limits, missing budget or currency, and missing or past expiry; it states spend authority is not implied. It is a pure check; no call path in non-test code invokes it with a real authorisation (grep: only `chat_eval.py` itself).
* `heldout_batch.py` enforces a USD hard cap of 5.00, at most 50 calls, token reservation and expiry re-check before every dispatch, but measures single-turn held-out proposals (#432 AC3, #435 AC4), not chat evaluation, and the CLI wires no live provider.
* `ai_registry.py` registers `chat-case-conversation`: `enabled False`, `state disabled`, accountable function Retrofit Programme Manager, accountable individual `UNKNOWN`, thresholds status `proposed`, `approved_by` None, `authorizes_live` False (test `test_chat_task_is_registered_disabled_with_reviewer_and_unapproved_thresholds`).
* Runtime chat calls go through core `Ai` admission and `DispatchHeld` (`test_chat_model.py`: denied admission makes no provider call), a runtime consumption control, not an evaluation authorisation.

## Findings

* No criterion is 100% proven by merged code and tests.
* Criterion 2 awaits human approval: thresholds are `proposed`, the named reviewer is `UNKNOWN`. Registration and disabled state are delivered; approval cannot be supplied by an agent.
* Criterion 1 is proven only for scripted and component scope; "pass before enablement" against an actual model and integrated memory is explicitly not covered.
* Criterion 3 has a tested fail-closed guard but no owner authorisation exists, no chat-evaluation call has been made, and the guard is not wired to a chat evaluation call path.

## Planning Readiness

Ready: produce a per-criterion proof table in the changes record, no ticks, no GitHub edits.
