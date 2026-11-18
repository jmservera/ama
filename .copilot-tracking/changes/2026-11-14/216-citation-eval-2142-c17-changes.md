<!-- markdownlint-disable-file -->
# Changes Record: Child Hardening Pass 17 for Issue #216 (`RV-044`..`RV-046`)

* Task ID: `216-citation-eval-2142-c17`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c17-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c17-phase-details.md`
* Critique Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c17-plan-critique.md`
* Status: `Completed`

## Summary

Completed `P01-T01` and `P01-T02` in `src/core` closing `RV-044`..`RV-046`:

### `P01-T01`: Refusal Precision (`RV-044`, `RV-046`) and Ship-Gated `ask()` Grounding (`RV-045`)

* Updated `_OBLIGATION_OBJECT_RE` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` to support quantified `of` determiner phrases (`all of our`, `any of the`, `each of these`, `every one of its`) while preserving the immediate post-verb `_OBLIGATION_PREPOSITION_GUARD_RE` guard (`RV-044`).
* Refined `_REFUSAL_PATTERNS[1]` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` so declarative progressive `meeting` clauses stay anchored to non-WH clause starts (`?!what\b|which\b|when\b|where\b|how\b|who\b|why\b`) while subordinate `whether|if|that` clauses match only after explicit compliance-inquiry verbs (`confirm`, `verify`, `certify`, `declare`, `state`, `say`, `check`, `tell me`, `decide`, `know`, `advise`, `assess`, `determine`, `judge`), preserving informational conditional WH-questions (`RV-046`).
* Added `verify_reply_grounding(bundle, chat_reply)` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` (reused by `resolve_regulatory_surface`) and enforced both canonical `refuse_question` and `verify_reply_grounding(snap, reply)` inside `RegulatoryChat.ask()` in `src/core/src/zava_forward/core/regulatory_chat.py` whenever `self.enforce_ship_gate` is `True`, raising `ChatForbidden` before persisting any ungrounded turn (`RV-045`).

### `P01-T02`: Regression Tests, Documentation, and Verification

* Added `test_c17_quantified_obligation_refusal_wh_conditional_precision_and_ask_grounding_gate` in `src/core/tests/test_regulatory_eval_gates_216.py` and updated `src/core/README.md`.
* Verified in `src/core`:
  * `python3 -m mypy`: `Success: no issues found in 318 source files`
  * `python3 -m ruff check .`: `All checks passed!`
  * `python3 -m ruff format --check .`: `265 files already formatted`
  * `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 20 tests ... OK`
  * `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`: `Ran 58 tests ... OK`

## Blockers and Remaining Work

* Blockers: None.
* Remaining active-plan work: None (`P01`, `P01-T01`, and `P01-T02` completed).
* Follow-up items (out of `src/core` scope): wire `src/api` and `src/agents` to `RegulatoryChat.ship_gated(...)` in a cross-package PR; populate ratified finance policy values once `BRD OD-51` closes.
