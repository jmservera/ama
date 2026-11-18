<!-- markdownlint-disable-file -->
# RPI Changes: Issue #216 Citation & Refusal Gates and Paired Rule-Card Comparison in `src/core`

## Metadata

* Task ID: 216-citation-eval-2142
* Related plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: Implemented `src/core/src/zava_forward/core/regulatory_eval_gates.py`, added end-to-end SQLite and `RegulatoryChat` verification in `src/core/tests/test_regulatory_eval_gates_216.py`, documented the module in `src/core/README.md`, and passed bare `mypy` (`strict = true`), `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*216*.py' -v`, `test_dependency_rule.py`, `test_regulatory_chat.py`, `test_gates.py`, and `test_live_doc_links.py`.

## Execution Summary

Delivered both remaining locally verifiable acceptance criteria for Issue #216 inside `src/core` without touching `src/agents` or relaxing `pyproject.toml`:

1. Owned citation-validity and refusal-accuracy gates (`GATE_OWNERS`, `PROVISIONAL_THRESHOLDS`, `GATE_RULES`, `DEFAULT_EVAL_CASES`, `ADVERSARIAL_PROMPTS`, `grade_chat_turn`, `agreement_gaps`, `evaluate_citation_and_refusal_gates`) measured across both the graded set and the adversarial set, emitting `GateResult` records (`unknown` under provisional unagreed targets, `fail` on threshold breaches or missing sets, `pass` only with a valid independent `OwnerGateAgreement`).
2. Deterministic rule-card projection and paired value comparator (`deterministic_rule_cards`, `authorise_model_run`, `cost_per_accepted_check`, `compare_chat_against_rule_cards`, `resolve_regulatory_surface`) comparing extractive chat against deterministic rule cards with provision links across active link parity, paired completion/comprehension/total-effort lift for `repairs`, `housing`, and `grants`, critical hazard misses, and beside-cost economics, enforcing `ship_mode = "cards_only"` (`cards_alone = True`, `chat = None`) whenever chat lacks measured value.

## Completed Work

### Core Regulatory Evaluation Gates and Paired Rule-Card Comparator (`P01`, `P01-T01`, `P01-T02`)

* Added `src/core/src/zava_forward/core/regulatory_eval_gates.py` with strict typing (`mypy` `strict = true`, zero `type: ignore` comments) and zero cross-package imports (`ALLOWED = {"core"}`).
* Defined named gate owners (`Legal and Regulatory Gate Owner` for `citation_validity` and `refusal_accuracy`; `Compliance, Safety and Programme Gate Owner` for `rule_card_value_comparison`), provisional 100% accuracy targets (`PROVISIONAL_THRESHOLDS`), and `GateRule` records (`GATE_RULES`, `effective_date = "2026-10-16"`).
* Implemented core-native extractive callbacks (`classify_purpose`, `refuse_question`, `render_extractive_answer`), `DEFAULT_EVAL_CASES` (7 graded + 6 adversarial scenarios) + `ADVERSARIAL_PROMPTS` (10 standalone adversarial prompts), `case_set_digest` (hashing pre-run case definitions and prompts while excluding `actual` outputs), `grade_chat_turn` (key-order independent section verification for `json.dumps(..., sort_keys=True)` persisted messages), `agreement_gaps`, and `evaluate_citation_and_refusal_gates` (`overall_pass = None`).
* Implemented `deterministic_rule_cards` (correlating provision links per card via `source_freshness` `source_id`), `authorise_model_run` (strict UTC expiry, positive finite USD cap, and `model-evaluation` run purpose), `cost_per_accepted_check`, `compare_chat_against_rule_cards`, and `resolve_regulatory_surface` enforcing `ship_mode = "cards_only"` (`cards_alone = True`, `chat = None`) whenever measured value is absent or any safety, link, gate, or cost guard fails.

### End-to-End Core Verification and Component Documentation (`P02`, `P02-T01`, `P02-T02`)

* Added `src/core/tests/test_regulatory_eval_gates_216.py` exercising live `RegulatoryChat` execution over both JSON `Store` and SQLite `SqlStore` across supported answers, stale monitoring-cadence labels, conflicting source versions and automatic referral, missing/future/partial/held empty-bundle abstentions, untrusted prompt-injection provisions, and adversarial prompts, plus negative gate mutations, owner-agreement validation, default `cards_only` shipping, full measured-lift `chat_with_cards` shipping, zero-lift/hazard/link/cost fallback to `cards_only`, and boolean/NaN/overflow/naive-datetime fail-closed guards. Included a worktree `sys.path` bootstrap so bare `unittest discover -s tests -p 'test_*216*.py' -v` loads this worktree's `zava_forward.core` even when another checkout is editable-installed in user site-packages.
* Documented `zava_forward.core.regulatory_eval_gates` (#216) in `src/core/README.md` alongside the #208/#214 regulatory chat subsections.

## Implementation-Time Plan and Detail Updates

* Local judgment (`P01-T01`): Changed `grade_chat_turn` section key validation from tuple order equality to key-set equality (`set(sections.keys()) == set(SECTION_KEYS)`) because `RegulatoryChat.encode` serializes stored turns with `json.dumps(..., sort_keys=True)`.
* Local judgment (`P02-T01`): Prepended the current worktree's `src/core/src` path in `test_regulatory_eval_gates_216.py` before importing `zava_forward.core` so bare `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` always exercises the active worktree without mutating shared editable `.pth` files.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` (`strict = true`, 318 files) | Passed | `Success: no issues found in 318 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` | Passed | `265 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` | `src/core/tests/test_regulatory_eval_gates_216.py` | Passed | `Ran 7 tests ... OK` |
| `python3 -m unittest discover -s tests -p 'test_dependency_rule.py' -v` | `src/core/tests/test_dependency_rule.py` | Passed | `Ran 2 tests ... OK` (`ALLOWED = {"core"}`) |
| `python3 -m unittest discover -s tests -p 'test_regulatory_chat.py' -v` | `src/core/tests/test_regulatory_chat.py` | Passed | `Ran 25 tests ... OK` |
| `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_gates.py' -v` | `src/core/tests/test_gates.py` | Passed | `Ran 31 tests ... OK` |
| `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_live_doc_links.py' -v` | `src/core/tests/test_live_doc_links.py` | Passed | `Ran 2 tests ... OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]`)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled
* Review readiness: ready for `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-plan.md, `## Follow-Up Items`
* Operational owner threshold agreement and independent held-out legal benchmark: Outside local code scope; owned by Legal, Compliance, and DPO before live chat enablement.
* Live repairs, housing, and grants staff paired trial with dated price source and spend authority: Outside local code scope; `cards_only` ships deterministic rule cards with provision links alone until measured.
* Optional refactoring in `src/agents`: Delegate duplicated pure evaluation logic in `src/agents/src/zava_forward/agents/regulatory_chat/` (`gate_agreement.py`, `paired_trial.py`, `citation_card_gates.py`) to `zava_forward.core.regulatory_eval_gates` in a dedicated `src/agents` cleanup task.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` completed)
* Validation coverage: `mypy`, `ruff check`, `ruff format --check`, `test_*216*.py`, `test_dependency_rule.py`, `test_regulatory_chat.py`, `test_gates.py`, and `test_live_doc_links.py` all passed
* Blockers: none
* Current plan and detail updates: recorded two local judgments (key-order-independent section check for `sort_keys=True` persistence and worktree `sys.path` test bootstrap)
* Planning and critique state: Ready (`PC-001`..`PC-004` resolved)
* Follow-up items: operational governance, live staff trial, and optional `src/agents` deduplication
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
