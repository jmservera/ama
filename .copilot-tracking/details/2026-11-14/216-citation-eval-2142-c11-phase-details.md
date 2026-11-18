<!-- markdownlint-disable-file -->
# Phase Details: Issue #216 Child Hardening Pass 11 (`216-citation-eval-2142-c11`)

* Task ID: `216-citation-eval-2142-c11`
* Date: `2026-11-14`
* Plan Artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c11-plan.md`

<!-- P01 -->
## Phase 1 (`P01`): Exact Per-Card Provision Linkage, Unflagged Version-Conflict Rejection, and Expected-Collection Guards

<!-- P01-T01 -->
### Task `P01-T01`: Production & Documentation Hardening (`src/core`)

* Target files:
  * `src/core/src/zava_forward/core/regulatory_chat.py`
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`
  * `src/core/README.md`
* Evidence-backed expectations:
  * `RegulatoryChat.bundle` (`C1`, `PC-004`): Add `"provision_ids": list(card["provisions"])` to emitted card dicts, and immediately after `if len(sources) > 4:`, if `result["refusal"]` is non-`None`, clear `result["sources"] = []`, `result["facts"] = []`, `result["cards"] = []`, `result["conflict"] = False` and return `result` before hazard-fact projection.
  * `_card_provenance_valid` & `_active_cards_link_provisions` (`C2`, `PC-001`):
    * Whenever `"provision_ids" in card`, require `_is_nonstr_seq(raw_pids)` (rejecting `None`), `len(raw_pids) > 0`, every `pid` `_is_utf8_str(pid) and bool(pid.strip()) and pid == pid.strip() and "#" in pid and _id_version_matches(pid, None, allow_fragment=True)`, no duplicate `pid`s, and `{pid.split("@v", 1)[0] for pid in raw_pids}` equal to the validated `source_freshness["sources"]` `source_id` set.
    * On conflict bundles/turns, require unique `source["id"]` and `card["id"]`, and for every card with `"provision_ids" in card`, require `set(card["provision_ids"]).issubset({src.get("id") for src in sources})`.
    * On active bundles/turns, `_active_cards_link_provisions` maps `[dict(prov) for prov in provisions if prov.get("id") in card_pid_set]` when `"provision_ids" in card`, and when `"provision_ids" not in card`, rejects multi-card ambiguity (`len(cards) > 1` with `sum(1 for prov in provisions if prov["id"].split("@v", 1)[0] == sid) > 1`). In `grade_chat_turn`, require `exp_linked is not None and act_linked == exp_linked` and matching `"provision_ids"` key presence across `(actual_card_mappings, expected_cards)`.
  * `_active_bundle_nonconflicting(sources, facts, cards)` (`C3`, `PC-003`):
    * Guard all accesses via `isinstance(..., Mapping)` and `.get(...)` and split version boundaries on `"@v"`.
    * Require unique `src.get("id")` across `sources`, and a single `(id_version_token, src.get("version"))` per base `source_id = sid.split("@v", 1)[0]`.
    * Require unique `fact.get("id")`, unique base fact path `fid.rsplit("@", 1)[0]` (when `"@"` in `fid`), and at most one distinct `fact.get("case_id")` across `facts`.
    * Require unique `card.get("id")` and unique base `card_id = cid.split("@v", 1)[0]` across `cards`.
    * Enforce in `_inspect_bundle_surface` (active branch) and `grade_chat_turn` (`require_active=True` branch in both `citations_ok` and `safe_fields_ok` for both `expected` and `actual`).
  * `grade_chat_turn`, `_classify_refusal_confusion`, & `_baseline_projection_matches` (`C4`, `PC-002`, `PC-004`):
    * Validate `raw_exp_sources`, `raw_exp_facts`, and `raw_exp_cards` unconditionally as `_is_nonstr_seq` of `Mapping`, preserving `expected_sources`, `expected_facts`, and `expected_cards` without pre-zeroing.
    * Enforce `len(expected_sources) == len(expected_facts) == len(expected_cards) == len(citations_seq) == len(actual_cards_seq) == 0` on `expected_kind == "refused"` and `len(expected_facts) == 0` on `expected_kind == "conflict"` in both `citations_ok` and `safe_fields_ok`.
    * Require `expected` self-consistency (`exp_self = grade_chat_turn(render_extractive_answer(expected), expected)` passing both `citation_validity` and `answer_contract`) before returning `"false_refusal"` in `_classify_refusal_confusion` and in `_baseline_projection_matches` when `not require_active_answer`.

<!-- P01-T02 -->
### Task `P01-T02`: Regression Tests & Validation (`src/core`)

* Target file: `src/core/tests/test_regulatory_eval_gates_216.py`
* Test ownership lock:
  * Exact removals: `none`
  * Maximum new test methods: `1` (`test_c11_exact_card_provision_ids_unflagged_version_conflicts_and_expected_refusal_guards`)
  * Coverage:
    1. Two active cards in `RegulatoryChat.bundle` citing two distinct provisions of the same source (`synthetic@v1#0001` and `synthetic@v1#0002`) map strictly to `[synthetic@v1#0001]` and `[synthetic@v1#0002]` in `deterministic_rule_cards`; stripping `"provision_ids"` on that two-card multi-provision bundle fails closed (`cards == []`, `kind == "refused"`), and mismatched `"provision_ids"` fails `grade_chat_turn`.
    2. Unflagged `conflict=False` bundles with `src@v1#0001` + `src@v2#0001`, `card@v1` + `card@v2`, or duplicate IDs fail closed across `deterministic_rule_cards`, `render_extractive_answer`, `_expected_from_bundle`, and `grade_chat_turn`.
    3. `grade_chat_turn` fails both `citation_validity` and `answer_contract` when `expected_kind == "refused"` has malformed or non-empty `sources`/`facts`/`cards` or when `expected_kind == "conflict"` has malformed or non-empty `facts`.
* Validation commands:
  * `cd src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*216*.py' -v`
  * `cd src/core && PYTHONPATH="src:tests" python3 -m unittest test_regulatory_chat test_gates test_live_doc_links -q`
