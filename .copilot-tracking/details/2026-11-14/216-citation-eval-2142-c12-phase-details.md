# Phase Details: Child Hardening Pass 12 for Issue #216 (`RV-026`..`RV-029`)

* Task ID: `216-citation-eval-2142-c12`
* Date: `2026-11-14`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md`
* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c12-research.md`

<!-- P01 -->
## Phase 1 (`P01`): Card-Signature Conflict, Freshness Aggregate Parity, and Surface Refusal Enforcement

<!-- P01-T01 -->
### Task `P01-T01`: Implement `RV-026`..`RV-028` in `regulatory_eval_gates.py`, `regulatory_chat.py`, and `src/core/README.md`

* Canonical targets:
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`
  * `src/core/src/zava_forward/core/regulatory_chat.py`
  * `src/core/README.md`
* Generated targets: `none`
* Evidence-backed expectations:
  * `RV-026` & `PC-001` (`C1`): In `_active_bundle_nonconflicting`, check `isinstance(card, Mapping)`, `safe_default = _nonblank_str(card.get("safe_default"))`, and `clock = _nonblank_str(card.get("clock"))`; return `False` when either is `None` (`_is_utf8_str` rejects non-`str` and `_UnhashableStr`), insert `(safe_default, clock)` into `signatures`, and return `False` if `len(signatures) > 1`.
  * `RV-027`, `PC-001`, & `PC-002` (`C2`):
    * Define `OUT_OF_CADENCE_LABEL = "Source out of monitoring cadence; ask the named owner."`.
    * In `_card_provenance_valid`:
      * Require `fresh_status = _nonblank_str(freshness.get("status"))` in `("in_cadence", "out_of_cadence", "unknown")`.
      * Require `fresh_label = _nonblank_str(freshness.get("label"))` is not `None`, and `(fresh_label == OUT_OF_CADENCE_LABEL) == (fresh_status == "out_of_cadence")`.
      * When `"as_of" in freshness`, require `fresh_as_of_day = _extract_day(freshness.get("as_of"))` is not `None`, and when `require_active and as_of_day is not None`, require `fresh_as_of_day == as_of_day`.
      * Require `raw_fresh_sources = freshness.get("sources")` unconditionally on all cards as a non-empty `_is_nonstr_seq` of `Mapping`, each with a nonblank unstripped `_is_utf8_str` `source_id` (unique per card).
      * If any constituent `entry` contains `"status"`, require every constituent `entry` in `raw_fresh_sources` to contain `"status"` with `_is_utf8_str` value in `("in_cadence", "out_of_cadence", "unknown")` and require aggregate `fresh_status` to equal `("out_of_cadence" if "out_of_cadence" in entry_statuses else "in_cadence" if all(s == "in_cadence" for s in entry_statuses) else "unknown")`.
      * On each constituent `entry`:
        * When `"as_of" in entry`, require `entry_as_of_day = _extract_day(entry.get("as_of"))` is not `None`, equals `fresh_as_of_day` if present, and equals `as_of_day` when `require_active and as_of_day is not None`.
        * When `"due_on" in entry`: if `entry["due_on"] is None`, require `entry.get("status") in (None, "unknown")`; else require `_valid_iso_day(entry["due_on"])`, and when `require_active and as_of_day is not None`, if `as_of_day >= entry["due_on"]`, require `entry.get("status") in (None, "out_of_cadence")` and `fresh_status == "out_of_cadence"`, and if `fresh_status == "in_cadence"`, require `as_of_day < entry["due_on"]`.
        * When `"last_success" in entry`: require `ls = entry["last_success"]` is `None` or `_valid_iso_day(ls)`; if `ls is None`, require `entry.get("due_on") is None` and `entry.get("status") in (None, "unknown")`; if `isinstance(ls, str)`, require `(not require_active or as_of_day is None or ls <= as_of_day)` and `(("due_on" not in entry) or (isinstance(entry["due_on"], str) and entry["due_on"] > ls))`.
        * When `"cadence_days" in entry`: require `cd = entry["cadence_days"]` is `None` or `(_strict_int(cd) is not None and 1 <= cd <= 36600)`; if `cd is None`, require `entry.get("last_success") is None`, `entry.get("due_on") is None`, and `entry.get("status") in (None, "unknown")`.
        * When `"last_success" in entry and "cadence_days" in entry` and `isinstance(entry["last_success"], str)` and `type(entry["cadence_days"]) is int`: require `entry.get("due_on") == (date.fromisoformat(entry["last_success"]) + timedelta(days=entry["cadence_days"])).isoformat()`.
      * When `"provision_ids" in card`, preserve exact `pid_base_sources == fresh_source_ids` parity.
    * In `_active_bundle_nonconflicting`:
      * Validate `isinstance(freshness, Mapping)` and non-empty `_is_nonstr_seq(freshness.get("sources"))`; for each `entry`, check `isinstance(entry, Mapping)`, nonblank unstripped `_is_utf8_str` `source_id`, and `val is None or _is_utf8_str(val)` on `status`, `due_on`, and `last_success` before storing `(entry.get("status"), entry.get("due_on"), entry.get("last_success"))` per `source_id`, returning `False` on any type mismatch or cross-card tuple disagreement.
      * Track enum `src.get("currentness")` in `("in_cadence", "out_of_cadence", "unknown")` per `base_sid` (rejecting conflicting enum `currentness` across provisions of the same `base_sid`); for every card referencing `base_sid`, if the constituent `entry` specifies `"status"`, require `entry["status"] == src_currentness`, and if `src_currentness == "out_of_cadence"`, require card aggregate `freshness.get("status") == "out_of_cadence"`.
    * In `_source_matches`: add `"currentness"` to `required_keys`.
    * In `grade_chat_turn` (`expected_kind == "answer"`):
      * Compute `exp_stale_card_present` across `expected_cards` and `stale_card_present` across `actual_cards_seq`.
      * When `"expect_out_of_cadence" in expected`, require `type(expected["expect_out_of_cadence"]) is bool and expected["expect_out_of_cadence"] == exp_stale_card_present`; otherwise set `expect_stale = exp_stale_card_present`.
      * Gate both `cards_prov_ok` (`citation_validity`) and `safe_fields_ok` (`answer_contract`) on `exp_expect_stale_ok and exp_stale_card_present == stale_card_present`.
  * `RV-028` (`C3`):
    * In `src/core/src/zava_forward/core/regulatory_chat.py`, import `refuse_question` from `.regulatory_eval_gates`.
    * In `RegulatoryChat.surface`, compute `canonical_refusal = refuse_question(question.strip()) or refuse_question(masked)`. When `canonical_refusal is not None`, set `snap = dict(sources=[], facts=[], cards=[], as_of=self.clock().isoformat(timespec="seconds"), conflict=False, refusal=canonical_refusal)` without trusting `self.refuse` to catch it; otherwise call `snap = self.bundle(user, cid, masked)`.

<!-- P01-T02 -->
### Task `P01-T02`: Apply `RV-029` fixture updates, add `test_c12` regression test, and validate

* Test ownership: `src/core/tests/test_regulatory_eval_gates_216.py`
* Exact removals: `none`
* Maximum additions: `1` (`test_c12_card_signature_conflict_freshness_consistency_and_surface_refusal_policy`)
* Semantic vs regression coverage:
  * Align `multi_bundle` cards on a shared `"safe_default": "Escalate to named human owner."` and update `v2_source["link"] = "/api/law/provisions/synthetic%40v2%230001"` in `test_c11` (`RV-029`).
  * Semantic & regression test `test_c12_...` verifying: (1) two active cards with divergent `clock` or `safe_default`—as well as unhashable `_UnhashableStr`/container card fields—fail closed without `TypeError` across `render_extractive_answer`, `deterministic_rule_cards`, and `grade_chat_turn` (`RV-026`, `PC-001`); (2) aggregate `in_cadence`/`unknown` card with an `out_of_cadence` or overdue `due_on` constituent source, forged `due_on=None` on `in_cadence`, tampered `due_on` vs `last_success`+`cadence_days`, missing/mismatched `out_of_cadence` label, mismatched `citations[0]["currentness"]` / source `currentness`, or non-boolean / contradictory `expect_out_of_cadence` fails closed while omitted-key stale bundle grading stays self-consistent (`RV-027`, `PC-002`); and (3) `RegulatoryChat.surface` initialized with a permissive `lambda _q: None` callback refuses a compound purpose-matching prohibited prompt under both `comparison=None` (`ship_mode == "cards_only"`, `chat is None`, `rule_cards["cards"] == []`) and verified `comparison=positive_cmp` (`ship_mode == "chat_with_cards"`, `chat["kind"] == "refused"`, `rule_cards["cards"] == []`) (`RV-028`, `PC-003`).
* Validation commands:
  * `cd /home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*216*.py' -v`
  * Companion regression check: `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_regulatory_chat.py' -q && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_gates.py' -q && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_live_doc_links.py' -q`
