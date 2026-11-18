<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #216 Child Closure (`RV-001`..`RV-006`) in `src/core`

## Metadata

* Task ID: 216-citation-eval-2142-c1
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c1-plan.md
* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c1-research.md

<!-- rpi:phase id=P01 -->
## P01: Close Fail-Open Grading, Binding, Link-Parity, and Overflow Defects (`RV-001`..`RV-006`)

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden `regulatory_eval_gates.py` for `RV-001`..`RV-006`

* Target file: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (and concise note in `src/core/README.md` if needed).
* Exact contracts:
  1. `RV-001` + `PC-001` (`grade_chat_turn`):
     * On `refused`: require `sections.get("what_sources_say") == "No verified active source quoted."` and `sections.get("recorded_home_facts") == "None quoted on a refused lookup."` in addition to exact `unknown_or_conflict == actual_refusal`, `safe_next_action == REFUSED_ACTION`, and `who_decides == REFUSED_DECIDER`.
     * On `conflict` and `answer`: compute `expected_what_say = "; ".join(f'[{s["id"]}] "{s["text"]}"' for s in expected_sources)` and `expected_recorded_facts = ("Withheld while cited source versions or rule cards conflict." if expected_kind == "conflict" else ("; ".join(f"[{f['id']}] {f['text']}" for f in expected_facts) if expected_facts else str(expected.get("unknown") or "No permitted structured home fact selected for this purpose.")))` and require exact equality (`what_say == expected_what_say` and `recorded_facts == expected_recorded_facts`). On `answer`, also require `sections.get("unknown_or_conflict") == (STALE_SNAPSHOT_NOTE if expect_stale else FRESH_SNAPSHOT_NOTE)` (with `stale_card_present` verified when `expect_stale` is `True`).
  2. `RV-002` + `PC-005` (`evaluated_outputs_digest` + `compare_chat_against_rule_cards`): Add `evaluated_outputs_digest(cases)` hashing canonical `(id, set_name, scenario, question, expected, actual)` for every case, emit `"evaluated_outputs_sha256": evaluated_outputs_digest(cases)` in `evaluate_citation_and_refusal_gates`, and require `isinstance(gates_report, Mapping) and gates_report.get("schema") == EVAL_SCHEMA and gates_report.get("evaluated_outputs_sha256") == evaluated_outputs_digest(cases)` inside `compare_chat_against_rule_cards`; when unbound, append an explicit blocking reason and reset `cit_check`/`ref_check` in `beside_cost` to `None`/`UNKNOWN`.
  3. `RV-003` (`_score_paired_observations` + `compare_chat_against_rule_cards`): Count `cards_hazard_misses` and `chat_hazard_misses` across all observations; if `(chat_hazard_misses + cards_hazard_misses) > 0`, mark `failure_severity = "critical"` and append a blocking reason in `compare_chat_against_rule_cards` so `measured_value` is `False` (`cards_only`).
  4. `RV-004` + `PC-004` (`agreement_gaps` + `_validate_benefit_thresholds`): In `agreement_gaps`, require `owner is not None and _canon_name(owner) == _canon_name(LEGAL_GATE_OWNER)` and reject self-grading on both full canonical name and parenthetical-stripped base person (`_canon_name(owner.split("(", 1)[0]) == _canon_name(grader.split("(", 1)[0])`, plus optional `owner_id` / `independent_grader_id` equality). In `_validate_benefit_thresholds`, require `owner is not None and _canon_name(owner) == _canon_name(COMPLIANCE_GATE_OWNER)`.
  5. `RV-005` + `PC-003` (`_score_structural_baseline`): Recompute `expected_rule_cards = deterministic_rule_cards(expected)` for each `answer` case; guard `isinstance` on `baseline`, `cards_list`, each `actual_card`, `provisions`, and `_nonblank_str` IDs before `urllib.parse.quote(..., safe="")`; require `len(cards_list) == len(expected_cards_list) > 0`, exact `(card_id, f"/api/law/cards/{quote(card_id.split('@', 1)[0], safe='')}")` per card (matching `RegulatoryChat.bundle` where `card["id"]` is `f"{card_id}@{version}"` while `card["link"]` encodes `card_id`), exact per-card `[(pid, f"/api/law/provisions/{quote(pid, safe='')}") ...]` parity against `expected_card["provisions"]`, exact top-level `provisions` `(pid, link)` parity when `baseline.get("provisions")` is present, and full coverage of `expected_source_ids`.
  6. `RV-006` + `PC-002` (`cost_per_accepted_check` + `resolve_regulatory_surface`): Convert `in_tokens`, `out_tokens`, and `accepted_count` via `_finite_float` after `_strict_int` validation before float division so `10**400` in either token counts or `accepted_checks` returns `"Unknown"` cleanly without `OverflowError`. Also verify `comparison.get("schema") == COMPARISON_SCHEMA`, `chat_reply.get("schema") == CHAT_SCHEMA`, `chat_reply.get("requires_human") is True`, and `chat_reply.get("operational_approval") is False` in `resolve_regulatory_surface`.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add regression assertions in `test_regulatory_eval_gates_216.py` and run `src/core` checks

* Target file: `src/core/tests/test_regulatory_eval_gates_216.py` (0 test removals, 0 new test files).
* Semantic and regression assertions to add:
  * Appended unsupported claim (`" This home is legally compliant."`) in `what_sources_say` / `reply` fails `grade_chat_turn` and `evaluate_citation_and_refusal_gates` (`RV-001`).
  * Mutating an evaluated case's `actual` after computing a passing `gates_report` fails `compare_chat_against_rule_cards` due to `evaluated_outputs_sha256` mismatch (`RV-002`).
  * Setting `hazard_missed = True` on a `cards`-arm observation yields `failure_severity == "critical"` and `ship_mode == "cards_only"` (`RV-003`).
  * Supplying an unrelated non-blank owner in `agreement` or `benefit_thresholds` fails closed (`RV-004`).
  * Multi-card per-card provision swap or wrong card/provision URL suffix fails `_score_structural_baseline` and reverts to `cards_only` (`RV-005`).
  * Passing `input_tokens = 10**400` to `cost_per_accepted_check` returns `"Unknown"` without raising `OverflowError` (`RV-006`).
* Verification commands:
  * `cd src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*216*.py' -v && python3 -m unittest discover -s tests -p 'test_dependency_rule.py' -v`
