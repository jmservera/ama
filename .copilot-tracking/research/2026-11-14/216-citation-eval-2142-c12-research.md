# RPI Research: Child Hardening Pass 12 for Issue #216 (`RV-026`..`RV-029`)

* Task ID: `216-citation-eval-2142-c12`
* Date: `2026-11-14`
* Output Mode: `convergence`
* Research Posture: `focused` (bounded internal hardening task within `src/core` from `216-citation-eval-2142-c11-review.md`)
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Research Brief

* Topic: Resolve `RV-026`..`RV-029` in `src/core` for Issue #216 (`regulatory_eval_gates.py`, `regulatory_chat.py`, `test_regulatory_eval_gates_216.py`, `src/core/README.md`).
* Scope: Strictly `src/core`; `src/api` and `src/agents` remain out of scope.
* Questions:
  1. `Q1` (`RV-026`): How does `RegulatoryChat.bundle` determine card-level conflict across multiple active cards, and how must `_active_bundle_nonconflicting` enforce that invariant?
  2. `Q2` (`RV-027`): What aggregate/constituent invariants does `card_freshness` enforce in `source_monitor.py`, and how should `_card_provenance_valid`, `_active_bundle_nonconflicting`, and `grade_chat_turn` prevent stale sources from being masked?
  3. `Q3` (`RV-028`): How should `RegulatoryChat.surface` enforce the canonically evaluated `refuse_question` policy even if an injected `self.refuse` callback misses a prohibited prompt?
  4. `Q4` (`RV-029`): How should `test_c11` isolate `_active_bundle_nonconflicting` on `v2_source` and align synthetic multi-card fixtures?

## Extension Registry & Participation

* Applied repository instructions (`.github/copilot-instructions.md`) and `rpi-research` contract.
* Inline 3-wave cycle (`wider`, `deeper`, `contrarian`) executed directly on the bounded 4-finding `src/core` target set (no independent external lane warranted).

## Cycle 1: Three-Wave Investigation

### Wave 1 — Wider

* Surveyed `RegulatoryChat.bundle` (`src/core/src/zava_forward/core/regulatory_chat.py:309-313`), `RegulatoryChat.surface` (`src/core/src/zava_forward/core/regulatory_chat.py:456-488`), `source_freshness` and `card_freshness` (`src/core/src/zava_forward/core/source_monitor.py:46-126`), `_active_bundle_nonconflicting` and `_card_provenance_valid` (`src/core/src/zava_forward/core/regulatory_eval_gates.py:680-735`, `1290-1340`), and `multi_bundle` / `test_c11` (`src/core/tests/test_regulatory_eval_gates_216.py:846-916`, `2489-2502`).

### Wave 2 — Deeper

* `C1` (`src/core/src/zava_forward/core/regulatory_chat.py:309-312` & `src/core/src/zava_forward/core/regulatory_eval_gates.py:680-735`): `RegulatoryChat.bundle` collects `signatures.add((card["safe_default"], card["clock"]))` and sets `result["conflict"] |= len(signatures) > 1`. Consequently, any legitimate `conflict=False` active bundle has `len({(card.get("safe_default"), card.get("clock")) for card in cards}) <= 1`. Note that synthetic `multi_bundle` (`src/core/tests/test_regulatory_eval_gates_216.py:892,907`) used two distinct `safe_default` strings only as placeholder text while testing two-source linkage; aligning `multi_bundle`'s two cards on one `(safe_default, clock)` matches `RegulatoryChat.bundle`'s exact `conflict=False` contract while rejecting conflicting card clocks or safe defaults in `_active_bundle_nonconflicting`.
* `C2` (`src/core/src/zava_forward/core/source_monitor.py:109-125` & `src/core/src/zava_forward/core/regulatory_eval_gates.py:1290-1340`, `1600-1616`): `card_freshness` restricts `status` to `("in_cadence", "out_of_cadence", "unknown")` using `"out_of_cadence"` if any constituent source is `"out_of_cadence"`, else `"in_cadence"` if non-empty and all constituent sources are `"in_cadence"`, else `"unknown"`, with mandatory label `"Source out of monitoring cadence; ask the named owner."` when `"out_of_cadence"`. Furthermore, `source_freshness` sets `"out_of_cadence"` whenever `current >= due_on`. Validating these aggregate-vs-constituent status/due-date/label rules inside `_card_provenance_valid`, cross-checking consistent per-`source_id` freshness and `src.get("currentness")` across `_active_bundle_nonconflicting`, and checking `stale_card_present == exp_stale_card_present` (and blocking `STALE_SNAPSHOT_NOTE` suppression when `exp_stale_card_present` is `True`) in `grade_chat_turn` closes `RV-027`.
* `C3` (`src/core/src/zava_forward/core/regulatory_chat.py:456-488`): `RegulatoryChat.surface` calls `masked = redact(question.strip())[0]` and `snap = self.bundle(user, cid, masked)`. Importing `refuse_question` from `.regulatory_eval_gates` and checking `canonical_refusal = refuse_question(question.strip()) or refuse_question(masked)` in `RegulatoryChat.surface` (replacing `snap` with an empty refused bundle carrying `refusal=canonical_refusal` whenever `canonical_refusal is not None`, after `admit` and case/question validation) ensures the shipped surface always enforces the evaluated refusal policy regardless of `self.refuse`.
* `C4` (`src/core/tests/test_regulatory_eval_gates_216.py:2492-2501`): Setting `v2_source["link"] = "/api/law/provisions/synthetic%40v2%230001"` makes `v2_source` individually provenance-valid so `unflagged_v1_v2` isolates `_active_bundle_nonconflicting`.

### Wave 3 — Contrarian

* Tested whether legacy synthetic fixtures (`multi_bundle` at `test_regulatory_eval_gates_216.py:894-913` and `unmapped_bundle` at `1178-1182`) omit per-entry `"status"` inside `source_freshness["sources"]` (`[{"source_id": "src-alpha"}]`): confirmed they omit per-entry `"status"` while setting card-level `"status": "in_cadence"`. Therefore `_card_provenance_valid` must validate `raw_fresh_sources` (`_is_nonstr_seq` of `Mapping` with valid `source_id`) unconditionally on all cards, and whenever any constituent `entry` includes `"status"` or `"due_on"`, enforce exact aggregate parity (`"out_of_cadence"` wins; `"in_cadence"` requires all present constituent statuses `"in_cadence"` and `as_of_day < due_on`; `"unknown"` forbids any `"out_of_cadence"` constituent or overdue `due_on`). Also require every constituent entry in a single `sources` list to either all carry `"status"` or be status-less minimal fixtures so mixed partial suppression (`[{"source_id": "a", "status": "in_cadence"}, {"source_id": "b"}]`) cannot hide an overdue source!
* Tested whether `expect_out_of_cadence` in `expected` can legitimately be `False` when an active card has `source_freshness["status"] == "out_of_cadence"`: NO — `render_extractive_answer` unconditionally emits `STALE_SNAPSHOT_NOTE` whenever any active card has `status == "out_of_cadence"`. Requiring `expect_stale == exp_stale_card_present == stale_card_present` in `grade_chat_turn` rejects both forged answers and inconsistent `expected` ground truth!

## Synthesis & Decision State

* Selected recommendation: Implement `C1`..`C4` directly in a single bounded `src/core` phase (`P01`).
* Rejected alternative: Mutating `RegulatoryChat.bundle` to override `self.refuse` globally — `RegulatoryChat.ask` and `RegulatoryChat.bundle` intentionally test injectable `refuse` callbacks in `test_regulatory_chat.py` and `evaluate_adversarial_prompts`, whereas `RegulatoryChat.surface` is the shipping surface selector where enforcing `refuse_question(question.strip()) or refuse_question(masked)` closes `RV-028` without breaking callback unit tests.
* Planning Readiness: `Ready`.
