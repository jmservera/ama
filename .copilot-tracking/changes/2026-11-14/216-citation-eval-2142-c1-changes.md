<!-- markdownlint-disable-file -->
# RPI Changes: Issue #216 Child Closure (`RV-001`..`RV-006`) in `src/core`

## Metadata

* Task ID: 216-citation-eval-2142-c1
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c1-plan.md
* Declared scope: Full plan (`P01`)
* Execution status: Completed (`P01` complete; reconciled for Review)

## Completed Work

### P01: Close Fail-Open Grading, Binding, Link-Parity, and Overflow Defects (`RV-001`..`RV-006`)

* `P01-T01` (`src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/README.md`):
  * Enforced exact canonical extractive strings in `grade_chat_turn` across `answer`, `conflict`, and `refused` turns (`what_sources_say`, `recorded_home_facts` with `expected.get("unknown")` fallback, `unknown_or_conflict` exact `STALE_SNAPSHOT_NOTE` / `FRESH_SNAPSHOT_NOTE`, `safe_next_action`, and `who_decides`), plus exact URL-encoded `/api/law/provisions/{quote(id, safe='')}` link verification in `_source_matches` (`RV-001`, `PC-001`).
  * Added `evaluated_outputs_digest(cases)` and emitted `evaluated_outputs_sha256` from `evaluate_citation_and_refusal_gates`; required `gates_report["schema"] == EVAL_SCHEMA` and `gates_report["evaluated_outputs_sha256"] == evaluated_outputs_digest(cases)` in `compare_chat_against_rule_cards`, resetting unbound `beside_cost` gate outcomes to `UNKNOWN` (`RV-002`, `PC-005`).
  * Marked `failure_severity = "critical"` and blocked `measured_value` whenever either `chat_hazard_misses > 0` or `cards_hazard_misses > 0` across paired or unpaired observations (`RV-003`).
  * Bound `OwnerGateAgreement["owner"]` to `LEGAL_GATE_OWNER` (and optional `refusal_owner` to `COMPLIANCE_GATE_OWNER`), rejected same-person parenthetical capacity aliases (`_base_person`) and matching `owner_id` / `independent_grader_id`, bound `benefit_thresholds["owner"]` to `COMPLIANCE_GATE_OWNER`, and bound `accepted_definition["owner"]` to `{COMPLIANCE_GATE_OWNER, LEGAL_GATE_OWNER}` (`RV-004`, `PC-004`).
  * Added `_exact_card_links_match` checking exact `/api/law/cards/{quote(card_id.split('@', 1)[0], safe='')}` card links (immediate current-state alignment with `RegulatoryChat.bundle` where `card["id"]` carries `@version` while `card["link"]` encodes `card_id`), exact `/api/law/provisions/{quote(pid, safe='')}` provision links, and exact 1:1 per-card `provisions` parity against `deterministic_rule_cards(expected)` (`RV-005`, `PC-003`).
  * Converted `in_tokens`, `out_tokens`, and `accepted_count` via `_finite_float` after `_strict_int` checks in `cost_per_accepted_check` so extreme integers (`10**400`) return `"Unknown"` without `OverflowError`, and hardened `resolve_regulatory_surface` schema/human-boundary checks (`RV-006`, `PC-002`).
  * Updated `src/core/README.md` (`#216` subsection) to reflect exact `LEGAL_GATE_OWNER` / `COMPLIANCE_GATE_OWNER` constants, `evaluated_outputs_sha256` binding, exact per-card link parity, and `cards`-arm critical hazard checks.
* `P01-T02` (`src/core/tests/test_regulatory_eval_gates_216.py`):
  * Added regression assertions covering appended unsupported claims on `answer` and `refused` turns, post-gate `actual` tampering caught by `evaluated_outputs_sha256`, `cards`-arm `hazard_missed = True` triggering `critical` severity and `cards_only`, mismatched gate/threshold owners and same-person parenthetical grader aliases, wrong card link suffixes and swapped multi-card provisions, and `10**400` token / accepted-check overflow handling.

## Implementation Discoveries and Updates

* Immediate current-state detail alignment (`P01-T01`): `RegulatoryChat.bundle` formats `card["id"]` as `f"{card_id}@{version}"` while formatting `card["link"]` as `f"/api/law/cards/{quote(card_id, safe='')}"`. `_exact_card_links_match` verifies `expected_card_link = f"/api/law/cards/{quote(exp_cid.split('@', 1)[0], safe='')}"` against both `expected_card["link"]` and `actual_card["link"]`, preserving exact URL-encoded parity on both versioned (`synthetic-hazard@v1`) and unversioned (`card-alpha`) card IDs. Reflected in `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md`.

## Validation Evidence

* `python3 -m mypy` in `src/core`: Passed (`Success: no issues found in 318 source files`).
* `python3 -m ruff check .` in `src/core`: Passed (`All checks passed!`).
* `python3 -m ruff format --check .` in `src/core`: Passed (`265 files already formatted`).
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` in `src/core`: Passed (8 tests OK).
* `python3 -m unittest discover -s tests -p 'test_dependency_rule.py' -v` in `src/core`: Passed (2 tests OK).
* `python3 -m unittest discover -s tests -p 'test_live_doc_links.py' -v` in `src/core`: Passed (2 tests OK).
* `python3 -m unittest discover -s tests -p 'test_regulatory_chat.py' -q` in `src/core`: Passed (25 tests OK).
* `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_gates.py' -q` in `src/core`: Passed (31 tests OK).

## Blockers and Remaining Work

* Blockers: none
* Remaining work in scope: none (`P01` complete)
* Follow-up items:
  * Optional `src/agents` helper deduplication against `zava_forward.core.regulatory_eval_gates` (outside `src/core` scope).
  * Out-of-band human threshold sign-off, external held-out legal benchmark, and live staff paired trial with authorised pricing.
