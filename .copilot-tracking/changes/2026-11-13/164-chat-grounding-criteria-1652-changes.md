# Changes: #164 remaining acceptance criteria audit

Task `164-chat-grounding-criteria-1652`, 2026-11-13. Documentation-only audit; no source, knowledge-base, GitHub issue or remote change. Tier: Focused (documentation-only; classification basis: no executable, workflow, dependency, infrastructure or security-control file changed). Hosted CI was not observed because nothing is pushed.

Audited base: worktree HEAD `3ffb8c0e7`, an ancestor of `origin/main` `6f9bb5074`. `git diff HEAD origin/main` over `src/agents` and `src/core/.../ai_registry.py` is empty, so the audited code equals current main, including merged #1517, #1525 and #1531.

## Test run (venv `/tmp/venv-164-1652`, pip editable installs, removed before commit)

| Scope | Result |
| --- | --- |
| `src/core/tests/test_chat_*.py` | 119 tests OK |
| `src/api/tests/test_chat_*.py` (`PYTHONPATH=../core/tests:../agents/tests`) | 103 tests OK, 2 skipped |
| `src/agents/tests/test_chat_model.py` | 17 tests OK |
| `src/agents/tests/test_heldout_batch.py` | 40 tests OK |
| `src/agents/tests/test_chat_eval.py` (added: holds the gate, registry and call-limit tests) | 45 tests OK |

Passing tests prove only what each test asserts; none uses an actual serving model.

## Per-criterion proof table

Rule: a criterion is Proven only when merged code and a passing test satisfy every clause of its text and no human approval, actual-model result or owner authorisation is still missing.

| Criterion | Proven by merged code and tests | Missing for 100% proof | Verdict |
| --- | --- | --- | --- |
| Memory poisoning and prompt-injection scenarios pass before enablement | `GATE_CATEGORIES` in `chat_eval.py` include `prompt-injection` and `memory-poisoning`; `gate_results` marks a missing category insufficient; scripted golden scenarios pass; `test_chat_eval.py` covers a failing injection gate failing enablement and a stale memory scope not vouching. | Scope is a scripted provider over a synthetic store. `OPEN_ITEMS` and `INTEGRATED_MEMORY` state integrated memory poisoning is "not covered", isolation memory checks are component-only, refusal and action-claim checks are lexical and paraphrase-bypassable, and actual-model, held-out and human-exercise evidence is not produced. "Before enablement" cannot be met: `enablement_decision` returns `insufficient` and `state disabled`. | Not proven: evidence gap (actual-model and held-out adversarial evidence) |
| Thresholds are approved before a task is enabled; the chat task is registered with accountable reviewer and enable/disable state | Registration: `ai_registry` entry `chat-case-conversation` exists with `enabled False`, `state disabled`, accountable function Retrofit Programme Manager (`test_chat_task_is_registered_disabled_with_reviewer_and_unapproved_thresholds`). Gate ordering: `enablement_decision` treats thresholds without `approved_by` as missing and applies no threshold check (`test_unapproved_thresholds_are_not_applied`). | Thresholds status is `proposed` with `approved_by` None; accountable individual is `UNKNOWN`. Approval and naming a reviewer are human owner decisions; an agent cannot supply them. "Disabled" is the default only: `authorizes_live` is true when the owner-approved demo-only switch and demo profile are both configured (`ai_registry.demo_activation_honoured`), outside this criterion's approval path. | Not proven: awaiting human threshold approval and named reviewer (registration and disabled-by-default halves are delivered) |
| Any actual call used for chat evaluation stays within a finite, owner-authorised call, token, budget and expiry limit, and no spend authority is assumed or implied | `chat_eval.call_authorization` blocks a missing named owner, non-positive or exhausted call and token limits, a missing budget, currency or expiry, and an expired authorisation; its result states spend authority is not implied (`test_actual_calls_are_blocked_without_finite_unexpired_authorisation`). `heldout_batch.py` re-checks expiry before every dispatch, caps USD 5.00 and 50 calls and reserves worst-case cost (40 tests), but covers single-turn held-out proposals, not chat evaluation. Chat runtime calls use core `Ai` admission, which makes no provider call when denied (`test_chat_model.py`). | The chat guard is a pure check whose only non-test caller is `enablement_decision` with `auth=None`, reporting a constant `blocked`; no evaluation call is gated by it. Verified locally: `max_budget=inf` and `expires_at="zzz"` both return `within-limit` (no finiteness test on budget, expiry is a lexical string comparison, projected spend is not compared with the budget); no test covers these. No owner authorisation for a chat evaluation call appears in the inspected evidence, and the scripted report records only scripted calls. | Not proven: evidence gap (guard has untested finiteness and expiry-format holes and is unwired; owner authorisation absent) |

## Result

None of the three criteria is 100% proven. Do not tick any. One (thresholds, reviewer) awaits human approval; two need further evidence. This agrees with the latest #164 comment that no remaining criterion is accepted.

## Recommended follow-ups (not started)

* Owner: approve or reject the proposed thresholds and name the accountable reviewer.
* Owner: decide on provider handling and a finite call, token, budget and expiry authorisation before any actual chat evaluation call; until then none may run.
* Engineering, if the owner wants criterion 3 closed in code: harden `call_authorization` (finite budget, ISO expiry parse, projected spend against budget) with tests, then wire it to the evaluation call path.
