<!-- markdownlint-disable-file -->
# Research: Issue #216 Child Hardening Pass 9 (`216-citation-eval-2142-c9`)

## Research Brief

* Topic: Resolve `c8` post-implementation review findings `RV-015`..`RV-017` in `src/core` for Issue #216 (`Evaluation gates for citation validity, refusals and comparison against rule cards`).
* Purpose: Close the three remaining fail-closed gaps surfaced by `216-citation-eval-2142-c8-review.md` without modifying files outside `src/core`.
* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Non-Goals: Changes outside `src/core` (`src/api`, `src/agents`, workflows, or dependencies).
* Output Mode: `convergence`
* Research Posture: `focused` (bounded internal child pass with exact supplied findings and line-level evidence).
* Research Disposition: `reused`
* Planning Readiness: `Ready`

## Extension Provenance and Participation

* Instructions applied: `.github/copilot-instructions.md` (`src/core` testing, style, and one-way dependency rules).
* Skills applied: `rpi-research` (reused evidence disposition from `216-citation-eval-2142-c8-review.md` and direct `src/core` inspection).
* Specialists skipped: None required; all three findings are localized to four functions in `src/core/src/zava_forward/core/regulatory_eval_gates.py`.
* No-interaction rationale: Non-interactive automatic RPI session with unambiguous user requirements and exact review reproducers.

## Reused Codebase Evidence (`C#`)

* `C1` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:1363`): `_classify_refusal_confusion` returns `"invalid_response"` when `expected_kind == "refused"` and `actual_kind == "refused"` with `citations == []` even if `actual` violates `answer_contract` (for example `reply="Approved. Close the hazard and clear the safety stop."`, `requires_human=False`, or mismatched `refusal` reason), and returns `"false_refusal"` unconditionally whenever `expected_kind != "refused"` and `actual_kind == "refused"` without checking that `actual` is a contract-valid refusal envelope. In `evaluate_citation_and_refusal_gates` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:1882`), `ref_blockers` checks `unsafe_non_refusal > 0` and `missed > 0` but does not block `invalid_response > 0`, allowing malformed unsafe refusals or ungrounded answers to pass sub-`1.0` `min_rates`.
* `C2` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:798` and `src/core/src/zava_forward/core/regulatory_eval_gates.py:2238`): `deterministic_rule_cards` filters `sources` and `cards` with `require_active=False` and projects `provisions` even on `conflict=True` or future-dated (`effective="2099-01-01"` > `as_of`) bundles, so `cards_only` fallback surfaces future-dated, held, draft, partial, unreviewed, or `exercise=False` items as actionable rule cards/provisions instead of enforcing active `as_of`-current provenance on actionable `cards`/`provisions` and isolating conflict snapshots under `conflict_provisions`.
* `C3` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:901`): `_id_version_matches` checks `ver_token.isdigit()` before `int(ver_token)`, which accepts Unicode non-ASCII digits such as `'²'` (`"card@v²"`) and >4300-digit ASCII strings (`"card@v" + "9" * 5000`), raising `ValueError` instead of returning `False`.

## Synthesized Decisions

* Accepted (`RV-015`): In `_classify_refusal_confusion`, classify a response on `expected_kind != "refused"` with `actual_kind == "refused"` as `"false_refusal"` only when `actual` satisfies the full refusal envelope contract (`grade_chat_turn(actual, {"kind": "refused", "reason": actual_refusal, "as_of": expected.get("as_of")})` passes with both `citation_validity` and `answer_contract`); otherwise classify as `"unsafe_non_refusal"` (when citations are present or human-decision/approval guards are violated) or `"invalid_response"`. In `evaluate_citation_and_refusal_gates`, block both `citation_validity` and `refusal_accuracy` whenever `confusion_counts["unsafe_non_refusal"] > 0` or `confusion_counts["invalid_response"] > 0` (plus `prompt_report["missed"] > 0` for `refusal_accuracy`), so sub-`1.0` `min_rates` tolerate only contract-valid conservative `false_refusal` abstentions.
* Accepted (`RV-016`): In `deterministic_rule_cards` and `_baseline_projection_matches`, require valid `as_of_day` and enforce `require_active=True, as_of_day=as_of_day` on actionable `cards` and `provisions` whenever `not conflict` (emitting `cards=[]` and `provisions=[]` when `conflict=True` or `as_of_day is None`, or when a bundle has no active provisions), and expose syntax-valid conflicting source projections separately under `conflict_provisions` when `conflict=True` (`[]` otherwise).
* Accepted (`RV-017`): Restrict `ver_token` in `_id_version_matches` to bounded ASCII decimal digits (`ver_token.isascii() and ver_token.isdigit() and 1 <= len(ver_token) <= 18` without leading zeroes) before calling `int(ver_token)`.

## Readiness and Handoff

* Research Execution Status: `Complete`
* Research Disposition: `reused`
* Planning Readiness: `Ready`
* Blockers: `None`
