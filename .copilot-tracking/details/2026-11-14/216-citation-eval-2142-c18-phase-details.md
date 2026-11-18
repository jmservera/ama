<!-- markdownlint-disable-file -->
# Phase Details: Child Hardening Pass 18 for Issue #216 (`RV-047`..`RV-048`)

* Task ID: `216-citation-eval-2142-c18`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c18-plan.md`

## `P01-T01`: Bundle Mutation Isolation and Progressive `meeting` Clause Precision

* In `src/core/src/zava_forward/core/regulatory_chat.py`:
  * In `ask()` when `self.enforce_ship_gate` is `True`: invoke `raw_reply = self.render(copy.deepcopy(snap))`, require `isinstance(raw_reply, dict)`, copy via `reply = copy.deepcopy(raw_reply)`, and verify `verify_reply_grounding(snap, reply)` against the unmutated `snap`.
  * In `surface()`: invoke `rendered = self.render(copy.deepcopy(snap))` and deep-copy `rendered` when constructing `candidate_reply` before `resolve_regulatory_surface(snap, resolved_comparison, chat_reply=candidate_reply)`.
* In `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Update progressive `meeting` branches in `_REFUSAL_PATTERNS[1]`:
    1. Clause-initial declarative progressive without WH/conditional subordinators (`what|which|when|where|how|who|why|if|unless|whenever`) between clause boundary and `(?:is|are|was|were)\s+...meeting`.
    2. Indirect polar `\bwhether\s+` progressive compliance clause (`\bwhether\s+(?:(?!(?:what|which|when|where|how|who|why)\b)\S+\s+){1,8}(?:is|are|was|were)\s+...meeting`).
    3. Inquiry-governed `(?:if|that)` progressive compliance clause (`confirm`, `verify`, `certify`, `declare`, `state`, `say`, `check`, `tell`, `ask`, `see`, `decide`, `know`, `advise`, `assess`, `determine`, `judge`, with optional indirect object `me|us` before `if|that`).

## `P01-T02`: Tests, Docs, and Verification

* Add `test_c18_renderer_bundle_mutation_isolation_and_whether_vs_prefaced_wh_if_precision` in `src/core/tests/test_regulatory_eval_gates_216.py` testing:
  * In-place mutation of `snap` inside `render` fails closed in both `RegulatoryChat.ask()` (`ChatForbidden` with zero stored turns) and `RegulatoryChat.surface()` (`cards_alone` fallback).
  * `"What is the answer as to whether the team is meeting statutory obligations?"` and `"Can you tell us if the contractor is meeting all of our safety standards?"` refuse, while `"Could you explain what happens if the team is meeting statutory obligations?"` is allowed.
* Update `src/core/README.md` and run `mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*216*.py' -v`, and companion `src/core` tests.
