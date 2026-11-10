---
title: Review - constructed paired observations in the regulatory gate report (Refs #216, #208)
description: Single post-implementation review of the final local candidate
ms.date: 2026-11-10
---

## Execution

* Executed once after implement-done, by the implementing agent reading the final diff (`src/agents/evals/run_regulatory_gates.py`, `src/agents/tests/test_paired_report_command.py`, `src/agents/README.md`) against the plan, details, critique, brief boundaries and the #216 acceptance criteria. No nested agent. This is a self-review and is not the independent exact-head assessment, which the coordinator owns.
* Assessed boundary: pinned main `d52f20a5198de7269f39daf794911545aee01ced` plus the uncommitted candidate (three source files above, tracking evidence).

## Evidence observed during review

* New command-level tests: 18 OK, all 18 red before implementation (option unrecognised, exit 2).
* CI-equivalent agents suite (`PYTHONPATH=src/core/tests`, `python -m unittest discover -s tests -q` from `src/agents`): 327 tests OK. Targeted set (`test_paired_report_command test_paired_trial test_regulatory_gates test_regulatory_answers test_eval_registry test_gate_agreement test_alert_triage test_dependency_rule`): 77 OK.
* `ruff check .`, `ruff format --check .` and configured `mypy` (48 files) pass in `src/agents`; supplementary file-only `mypy --strict` of the script passes (not configured coverage).
* Default 60000-home command output is byte-identical to `regulatory_gates_results.json` (sha256 `8f97a758c61fbc82a149c4644d5ae0072ab1c0fd598ff6c59b2677a0ea973f7c`). With the option, the report minus the new section equals the committed report.
* `paired_trial.py`, `regulatory_gates.py` and the committed results are unchanged by hash; no `src/api`, `src/core`, `infra` or workflow edit.
* Guarded run test: network `connect` and `subprocess.Popen` patched to raise, command still succeeds; an absent `ZF_DATA` path is never created.

## Boundary check

| Boundary | Outcome |
| --- | --- |
| Existing scorer unchanged, no second scorer | Met; called once with `thresholds=None`, `cost_inputs=None` |
| Strict bounded input, explicit nonzero refusal | Met; size, count, shape, exact keys, types, finite, bounds, duplicate keys, pseudonymous ids; `SystemExit` messages, no broad catch |
| No threshold, price, budget, authority or approval input | Met; envelope accepts exactly `schema` and `observations` |
| Unknown cost with named inputs, `cards_only` for favourable input | Met; tested at command level |
| Distinct section, existing sections unchanged, no dataset merge | Met; tested by equality |
| Qualification: caller-declared constructed, unverified participation, not human acceptance | Met; wording tested |
| Default output unchanged; writes only via `--record` | Met |
| No model, provider, network, subprocess, ZF_DATA, deployment | Met within tested paths |

## Findings and routing (later work, none re-opened in this task)

| Id | Finding | Routing |
| --- | --- | --- |
| R1 | `--record` combined with the option can overwrite the canonical results file with constructed content. Existing semantics kept; README warns; no guard added. | Follow-up: owner decision on refusing `--record` with the option |
| R2 | The pseudonymous-id pattern cannot prove pseudonymity or exclude coded personal data. | Limit, stated in qualification and README |
| R3 | Self-critique and self-review only; no independent critique. | Coordinator independent exact-head assessment |
| R4 | The command tests take about 65 s because each report generation costs about 7 s of fixture setup; two shared runs plus one guarded run. | Optional later speed-up by making the fixture cheaper; not blocking |
| R5 | No mutation testing of the new tests. | Optional follow-up |
| R6 | One edit to the plan checkboxes used `sed -i` instead of the edit tool. Content effect: ticks phases 2 to 5 only. | Disclosed process deviation |
| R7 | No hosted CI observed (nothing pushed); no browser, SQL, model, human or live validation. | Coordinator after publication |

## Outcome

`conformant-with-limits` for the admitted slice. No material finding remains open inside the slice. #216 remains open: owner thresholds and independent grading (criterion 1), a real staff paired trial and measured chat value (criterion 4), AI cost per accepted check with real inputs, and an owner-authorised finite live run (tokenomics 1 and 2) are unmet. Nothing here claims or implies human acceptance, owner agreement or approval to ship chat.
