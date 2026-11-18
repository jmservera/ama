<!-- markdownlint-disable-file -->
# RPI Review: Issue #216 Child Closure (`216-citation-eval-2142-c1`)

## Metadata

* Task ID: 216-citation-eval-2142-c1
* Parent task: 216-citation-eval-2142
* Review date: 2026-11-14
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c1-research.md
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c1-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c1-changes.md
* Parent review: .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-review.md

## Boundary and Reconciliation Assessment

* Plan markers (`P01`, `P01-T01`, `P01-T02`), phase details, changes record, and validation results are reconciled.
* Independent read-only review (`rubber-duck`) verified closure of `RV-003`, `RV-004`, `RV-006`, and `PC-002`, and surfaced four remaining fail-closed hardening defects (`RV-001`..`RV-004` below) plus three defensive cleanups (`RV-005`..`RV-007`) routed to child task `216-citation-eval-2142-c2`.
* Descriptive implementation-time update on versioned rule-card IDs (`card["id"] = f"{card_id}@{version}"` vs `/api/law/cards/{quote(card_id, safe="")}`) preserves user intent and `RegulatoryChat.bundle` routing, but needs explicit endpoint-contract alignment and versioned-ID regression coverage (`RV-004`).
* Plan `## Follow-Up Items` (`src/agents` helper deduplication and out-of-band human governance/live trial prerequisites) remain distinct follow-ups outside `src/core` task scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Refused turns with `expected["reason"] = None` still accept appended claims inside `refusal` / `unknown_or_conflict`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`DEFAULT_EVAL_CASES` sets `expected_reason: None` on the five adversarial prompt cases, and `grade_chat_turn` allows `expected_reason is None` to accept any non-blank `actual["refusal"]` echoed into `sections["unknown_or_conflict"]`).
* Impact: Appending an unsupported compliance claim to `actual["refusal"]` and `sections["unknown_or_conflict"]` passes when `expected["reason"]` is `None`.
* Destination: `rpi-implement`
* Smallest useful next action: Populate exact canonical `expected_reason` strings across all refused `DEFAULT_EVAL_CASES` and require `expected_reason is not None and actual_refusal == expected_reason` in `grade_chat_turn` and `_classify_refusal_confusion`, with a negative test for appended claims in `refusal` / `unknown_or_conflict`.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: `gates_report` pass flags remain mutable after evaluation without report-level integrity verification

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`compare_chat_against_rule_cards` verifies `evaluated_outputs_sha256` against `cases`, but trusts `gates_report["checks"][*]["gate_met"]` without binding `threshold_status`, `agreement_gaps`, `dataset_gaps`, `gate_results`, and per-case grades via an integrity digest or direct re-verification).
* Impact: Flipping `gate_met` to `True` on a provisional `gates_report` preserves `evaluated_outputs_sha256` and can yield `measured_value = True`.
* Destination: `rpi-implement`
* Smallest useful next action: Emit `report_integrity_sha256` over the canonical gate evaluation summary (`case_set_sha256`, `evaluated_outputs_sha256`, `threshold_status`, `agreement_gaps`, `dataset_gaps`, and `checks`), verify `report_integrity_sha256`, `threshold_status == "owner_agreed"`, empty `agreement_gaps` / `dataset_gaps`, `gate_results[*].outcome == PASS`, and direct `grade_chat_turn` pass across `cases` in `compare_chat_against_rule_cards`, and add a regression test mutating `gate_met` on a provisional report.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: `resolve_regulatory_surface` checks envelope flags on `chat_reply` without verifying extractive grounding against `bundle`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`resolve_regulatory_surface` checks `schema`, `requires_human`, and `operational_approval` on `chat_reply`, without checking `workflow_only is True` or grading `chat_reply` against `bundle`).
* Impact: When `comparison["measured_value"]` is `True`, passing an ungraded or mismatched `chat_reply` (or `workflow_only = False`) could still be returned on the `"chat_with_cards"` surface.
* Destination: `rpi-implement`
* Smallest useful next action: Build expected ground truth directly from `bundle` inside `resolve_regulatory_surface` and require `grade_chat_turn(chat_reply, expected_from_bundle) == {"citation_validity": True, "answer_contract": True}` before enabling chat; otherwise fall back to `cards_only` with an explicit reason, and add a regression test.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Versioned card ID link contract (`card_id@version` -> `/api/law/cards/{card_id}`) lacks explicit documentation and multi-card `@version` test coverage

* Related scope: `P01-T01`, `P01-T02`
* Evidence: `RegulatoryChat.bundle` emits `card["id"] = f"{card_id}@{version}"` and `card["link"] = f"/api/law/cards/{quote(card_id, safe='')}"`, while `test_regulatory_eval_gates_216.py`'s multi-card fixture used unversioned `card-alpha` / `card-beta` IDs and `README.md` did not state the unversioned card-route vs versioned provision-route distinction.
* Impact: Readers or synthetic callers may confuse card route identity (`card_id`) with provision route identity (`provision_id` including `@version#section`).
* Destination: `rpi-implement`
* Smallest useful next action: Document `/api/law/cards/{quote(card_id, safe='')}` (`card_id = id.split("@", 1)[0]`) vs `/api/law/provisions/{quote(provision_id, safe='')}` in `regulatory_eval_gates.py` and `src/core/README.md`, and use versioned `card-alpha@v1` / `card-beta@v1` IDs in the multi-card test while asserting `/api/law/cards/card-alpha%40v1` is rejected.

<!-- rpi:review id=RV-005 -->
### RV-005 [Low]: `_score_structural_baseline` and `_exact_card_links_match` allow empty per-card provision lists on secondary cards and unguarded non-Mapping `paired_cards` entries

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_score_structural_baseline` calls `entry.get("id")` without guarding `isinstance(entry, Mapping)`, and `_exact_card_links_match` permits `len(act_card_provs) == len(exp_card_provs) == 0` when another card covers `expected_source_ids`).
* Impact: Non-Mapping entries in `paired_cards` raise `AttributeError`, and an active answer card with zero linked provisions can pass if a sibling card covers the provisions.
* Destination: `rpi-implement`
* Smallest useful next action: Guard `isinstance(entry, Mapping)` in `_score_structural_baseline`, require `len(act_card_provs) > 0` for every card in `_exact_card_links_match`, and add regression assertions.

<!-- rpi:review id=RV-006 -->
### RV-006 [Low]: `agreement_gaps` validates optional `refusal_owner` but ignores optional `compliance_owner`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`agreement_gaps` checks `"refusal_owner"` when present, but ignores `"compliance_owner"`).
* Impact: A caller passing a mismatched `"compliance_owner"` key receives no validation gap.
* Destination: `rpi-implement`
* Smallest useful next action: Validate both optional `"refusal_owner"` and optional `"compliance_owner"` against `COMPLIANCE_GATE_OWNER` in `agreement_gaps` and add a test case.

<!-- rpi:review id=RV-007 -->
### RV-007 [Low]: `_canon_json` does not recursively normalize nested custom `Mapping` / `Sequence` instances such as `UserDict`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`case_set_digest` and `evaluated_outputs_digest` shallow-copy top-level `expected` and `actual` mappings, so nested `collections.UserDict` values raise `TypeError` in `json.dumps`).
* Impact: Valid non-`dict` `Mapping` inputs inside nested case structures raise `TypeError` during digest computation.
* Destination: `rpi-implement`
* Smallest useful next action: Recursively normalize nested `Mapping` and non-string/bytes `Sequence` objects inside `_canon_json` and add a `UserDict` digest test.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001`..`RV-007` | `rpi-implement` | Child task `216-citation-eval-2142-c2` | Tightening fixes in `regulatory_eval_gates.py`, `test_regulatory_eval_gates_216.py`, and `src/core/README.md` |

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` (318 files) | Passed | Zero issues |
| `python3 -m ruff check .` | `src/core` | Passed | All checks passed |
| `python3 -m ruff format --check .` | `src/core` | Passed | 265 files formatted |
| `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` | `src/core/tests/test_regulatory_eval_gates_216.py` | Passed | 8 tests OK |
