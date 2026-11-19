# Research: issue 216 live2 (evaluation gates, rerun of existing gate tests)

Task: issue-216-live2. Refs #216. Synthetic demo, desktop only. Live Azure authorised (rg ama, cap USD 700); no drills, no Key Vault rotation, no production change.

Research disposition: executed (opening record; findings added below).

* Issue 216 has one unticked criterion: gates for citation validity and refusal accuracy set with owners and measured on a graded and adversarial set.
* A prior run (research note eval-gates-live-216-2026-11-18.md, merged in #1934) measured the live case chat: 7 of 7 model-path citations valid, refusals 10 of 10, 13 prompts not model-reached.
* This task keeps that evidence and adds: the existing core/agents gate tests run locally with raw output retained, and a rescoring of the saved raw container output to confirm it reproduces.
* Existing state file issue-216-live-state.json is not overwritten; this task uses issue-216-live2-state.json.

## Findings

* The saved raw container output (raw3.json) was not retained by the earlier run; only the scored `report-model-container.json` exists. Rescoring is therefore not possible; the container figures are "Observed; raw output not retained".
* Existing gate tests (core test_regulatory_eval_gates_216; agents test_regulatory_gates, test_regulatory_citation_card_gates, test_ai_eval, test_paired_trial, test_gate_agreement; core test_regulatory_output_guard) run locally: 101 tests OK. Raw output retained in docs/reference/research/eval-gates-live-216-2026-11-18/unit-tests-raw-2026-11-18.txt.
* A fresh live model run on the 13 unreached prompts is not repeated: the earlier exercise already exceeded the 45-call authorization declared in authorization.json, and the same-day demo meter is spent. Deferred to after 2026-11-19T00:00Z.
* Planning Readiness: Ready.
