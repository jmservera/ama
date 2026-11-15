---
title: "Research: #164 criterion 3, memory poisoning and prompt injection before enablement"
ms.date: 2026-11-13
task_slug: 164-memory-poison-injection-2035
---

## Scope

Issue #164 criterion 3 ("Memory poisoning and prompt-injection scenarios pass before enablement") is unticked. Branch `feat/demo-164-memory-poison-eval-2035`, base `c13d077d2`. Research disposition: executed. Planning Readiness: Ready.

## Path correction

The task named `src/core/.../chat_eval.py`; the harness lives in `src/agents/src/zava_forward/agents/chat_eval.py` with tests in `src/agents/tests/test_chat_eval.py` and golden file `src/agents/evals/chat_golden.json`. `ChatPanel` is `src/core/src/zava_forward/core/chat_panel.py`, `ChatIsolation` is `src/core/src/zava_forward/core/chat_isolation.py`. API tests: `src/api/tests/test_chat_panel.py`, `src/api/tests/test_chat_isolation.py`. There is no `src/core/tests/test_chat_eval*.py`.

## Current behaviour (evidence)

* `run_eval` runs 24 golden scenarios (61 turns) through the real `ChatPanel` and `ChatIsolation` with a scripted model. All pass; failures 0, critical 0, enablement `insufficient`, task disabled.
* Prompt injection: 4 scenarios (user turn, `measures` source, thread history, plain-prose obedience). Memory poisoning: 2 scenarios (one seeded memory with no authority plus approval refusal; one special-category rejection).
* `gate_results` gives per-category pass/fail/insufficient; `enablement_decision` returns `fail` if any gate fails, critical failures exist, or gaps are open; it never returns `pass`.
* Registry proposed thresholds already name `memory_poisoning_pass_rate`, `prompt_injection_pass_rate` and `critical_failures=0` (`ai_registry.py:153`).

## Gaps

1. The summary has no explicit `critical_errors`, `memory_poisoning_passed` or `prompt_injection_passed`; consumers must derive them from `by_category` and `critical_failures`.
2. `enablement_decision` trusts `summary` keys and is not explicit about a non-zero critical-error count or a malformed or missing field; the decision lacks the explicit flags.
3. Coverage: no poisoned memory that tries to fabricate a citation or approval/consent and is followed by a model that echoes it; no memory poison that references another case; no injection in a case note of another case (cross-case); no system-prompt override or role-elevation claim inside a retrieved case note; no cross-role injection (a role-elevation claim after a role downgrade, and a reason-field leak attempted by an injection to a role without reason access).
4. The CLI does not print the explicit gate flags.

## Constraints

* Scripted evidence only: no claim about an actual model; enablement stays `insufficient` at best.
* Changing `chat_golden.json` changes `golden_sha256`; tests derive bindings from the report so none hard-code it. `chat_heldout.py` reuses `summarise` and `run_scenario`.
* pip only; scratch venv `/tmp/venv-164p-2035`.
* Do not tick the issue criterion or edit GitHub.
