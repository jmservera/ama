<!-- markdownlint-disable-file -->
# Research Synthesis: Issue #216 Child Hardening Pass 11 (`216-citation-eval-2142-c11`)

* Task ID: `216-citation-eval-2142-c11`
* Parent Task ID: `216-citation-eval-2142-c10`
* Date: `2026-11-14`
* Output Mode: `convergence`
* Research Posture: `focused` (bounded internal hardening task with named `src/core` targets and exact review failure evidence)
* Research Execution Status: `Complete`
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Research Brief

* Topic: Close remaining in-scope `src/core` review defects `RV-023`, `RV-024`, and `RV-025` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c10-review.md`.
* Purpose & Audience: Provide verified codebase evidence for `rpi-plan` and `rpi-implement` in `src/core`.
* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Non-Goals: Out-of-scope edits to `src/api` or `src/agents`, or gating `RegulatoryChat.ask` (which is the offline turn-evaluation runner required prior to paired comparison).
* Initial Questions:
  * `Q1` (`RV-023`): How should `RegulatoryChat.bundle` and `_active_cards_link_provisions` bind cards to exact provision IDs when multiple provisions share a base `source_id`, without breaking synthetic single-provision-per-source bundles?
  * `Q2` (`RV-024`): How should `_inspect_bundle_surface` and `grade_chat_turn` detect unflagged source-version or duplicate-ID contradictions when `conflict=False`?
  * `Q3` (`RV-025`): Why did `grade_chat_turn` accept malformed or non-empty `expected["facts"]` and `expected["cards"]` on `refused` (and `expected["facts"]` on `conflict`) turns, and does strict validation preserve all 13 `DEFAULT_EVAL_CASES`?

## Extensions and Participation

* Selected instructions: Repository instructions (`.github/copilot-instructions.md` — `src/core` boundary, focused validation tier, zero `.copilot-tracking/` references in source/docs/commits).
* Skipped domain skills/subagents: Inline `focused` execution selected because all three uncertainties couple tightly to `regulatory_eval_gates.py` and `regulatory_chat.py` (fewer than 4 direct file reads).
* Intake interaction: None required; caller constraints and review findings fully specify the boundary.

## Cycle 1: Three-Wave Investigation

### Wave 1 — Wider

* Scanned `RegulatoryChat.bundle` (`src/core/src/zava_forward/core/regulatory_chat.py:251-326`), `card_freshness` (`src/core/src/zava_forward/core/source_monitor.py:96-126`), `_active_cards_link_provisions` and `_inspect_bundle_surface` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:648-845`), `grade_chat_turn` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:1235-1495`), `_baseline_projection_matches` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:2453-2530`), and all `["cards"]` assertions across `src/core/tests/`.

### Wave 2 — Deeper

* `C1` (`src/core/src/zava_forward/core/regulatory_chat.py:293-308` & `src/core/src/zava_forward/core/source_monitor.py:96-126`): Each rule card in `self.law.rules` carries exact `card["provisions"]` (`list[str]` of `source_id@vN#NNNN`), whereas `card_freshness` deduplicates `source_freshness["sources"]` by base `source_id`. Emitting `"provision_ids": list(card["provisions"])` in `RegulatoryChat.bundle` gives `_active_cards_link_provisions` exact per-card provision IDs while keeping projected card keys in `deterministic_rule_cards` unchanged.
* `C2` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:648-693`): `_active_cards_link_provisions` matches `prov["id"].split("@", 1)[0] in mapped_source_ids`. When `"provision_ids"` is present on a card, validating exact UTF-8 nonblank unstripped provision IDs against `provisions` and requiring `{pid.split("@", 1)[0] for pid in raw_pids} == mapped_source_ids` maps each card strictly to its own provisions. When `"provision_ids"` is omitted (synthetic fixtures such as `multi_bundle` at `src/core/tests/test_regulatory_eval_gates_216.py:846-916`), requiring unambiguous source-to-provision mapping (`len(cards) == 1` or `sum(1 for prov in provisions if prov["id"].split("@", 1)[0] == sid) == 1`) preserves 1-to-1 synthetic fixtures while failing closed whenever multi-card bundles reference a multi-provision source without `provision_ids`.
* `C3` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:759-838` & `1305-1340`): Neither `_inspect_bundle_surface` nor `grade_chat_turn` checks whether an unflagged `conflict=False` (`answer`) bundle contains multiple versions of the same base `source_id` (`src@v1#0001` and `src@v2#0001`), duplicate `source["id"]`s, duplicate `fact["id"]`s, or duplicate/conflicting base `card_id`s (`card@v1` and `card@v2`). Adding `_active_bundle_nonconflicting(sources, facts, cards)` to both `_inspect_bundle_surface` and `grade_chat_turn` (`require_active=True`) closes `RV-024`.
* `C4` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:1241-1300` & `1405-1435`): `grade_chat_turn` validates `raw_exp_facts` only when `expected_kind == "answer"` and `raw_exp_cards` only when `expected_kind != "refused"`, then overwrites `expected_facts = []` and `expected_cards = []` before line `1295` checks `len(expected_facts) == 0` and `len(expected_cards) == 0`. Validating `raw_exp_sources`, `raw_exp_facts`, and `raw_exp_cards` as `_is_nonstr_seq` of `Mapping` unconditionally, preserving all three lists, and requiring `len(expected_sources) == len(expected_facts) == len(expected_cards) == 0` on `refused` (in both `citations_ok` and `safe_fields_ok`) and `len(expected_facts) == 0` on `conflict` closes `RV-025`.

### Wave 3 — Contrarian

* Tested whether rejecting distinct `(safe_default, clock)` across multiple active cards would break valid multi-source bundles: `multi_bundle` (`src/core/tests/test_regulatory_eval_gates_216.py:846-916`) pairs two distinct regulations (`card-alpha@v1`, `card-beta@v1`) with distinct `safe_default` text (`"Escalate alpha..."` vs `"Escalate beta..."`). Therefore `_active_bundle_nonconflicting` must reject duplicate IDs and multi-version collisions per base `source_id` / base `card_id`, NOT distinct `(safe_default, clock)` across distinct cards.
* Tested whether strict `expected` emptiness checks on `refused` and `conflict` break any `DEFAULT_EVAL_CASES` scenario (`src/core/tests/test_regulatory_eval_gates_216.py:95-242`): all refused scenarios (`missing`, `future`, `partial`, `held`, and prompt-refused turns) produce `bundle["sources"] == []`, `bundle["facts"] == []`, `bundle["cards"] == []`, and `conflict` produces `bundle["facts"] == []`. Also checked `RegulatoryChat.bundle` when hitting `Too many relevant sources` (`src/core/src/zava_forward/core/regulatory_chat.py:289-292`) or `Too many conflicting versions` (`line 312`): clearing `result["sources"] = []`, `result["facts"] = []`, `result["cards"] = []`, `result["conflict"] = False` whenever `result["refusal"]` is set in `RegulatoryChat.bundle` ensures refused bundles never carry leftover partial cards/sources into naive callers either!

## Synthesis and Decision State

* Selected recommendation (`convergence`):
  1. Emit `"provision_ids": list(card["provisions"])` in `RegulatoryChat.bundle` and clear `sources`/`facts`/`cards`/`conflict` if `result["refusal"]` triggers mid-loop (`C1`).
  2. Enforce exact `"provision_ids"` validation and unambiguous fallback in `_card_provenance_valid` and `_active_cards_link_provisions` (`C2`).
  3. Enforce `_active_bundle_nonconflicting(sources, facts, cards)` (no duplicate source/fact/card IDs, no multi-version base `source_id` or base `card_id`) in `_inspect_bundle_surface` and `grade_chat_turn` for active non-conflict bundles (`C3`).
  4. Validate `raw_exp_sources`, `raw_exp_facts`, and `raw_exp_cards` unconditionally in `grade_chat_turn` without pre-zeroing them, requiring empty `sources`/`facts`/`cards` on `refused` and empty `facts` on `conflict` in both `citation_validity` and `answer_contract` (`C4`).
* Rejected alternatives:
  * Gating `RegulatoryChat.ask` on `comparison`: Rejected because `ask` is the offline evaluation runner that produces turns prior to `compare_chat_against_rule_cards`.
  * Rejecting distinct `(safe_default, clock)` across distinct active cards in `_active_bundle_nonconflicting`: Rejected via contrarian evidence from `multi_bundle` (`src/core/tests/test_regulatory_eval_gates_216.py:846-916`).
* Blockers / Unresolved Decisions: None.
* Planning Readiness: `Ready`.
