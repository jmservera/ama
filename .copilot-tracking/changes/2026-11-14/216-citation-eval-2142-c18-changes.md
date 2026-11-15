<!-- markdownlint-disable-file -->
# Changes Record: Child Hardening Pass 18 for Issue #216 (`RV-047`..`RV-048`)

* Task ID: `216-citation-eval-2142-c18`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c18-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c18-phase-details.md`
* Critique Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c18-plan-critique.md`
* Status: `Completed`

## Summary

Completed `P01-T01` and `P01-T02` in `src/core` closing `RV-047` and `RV-048`:

### `P01-T01`: Renderer Bundle Mutation Isolation (`RV-047`) and Progressive `meeting` Clause Precision (`RV-048`)

* Passed `copy.deepcopy(snap)` into `self.render(...)` and deep-copied returned mappings in both `RegulatoryChat.ask()` and `RegulatoryChat.surface()` in `src/core/src/zava_forward/core/regulatory_chat.py` so `verify_reply_grounding(snap, reply)` and `resolve_regulatory_surface(snap, ...)` always evaluate against an unmutated `snap` (`RV-047`).
* Refined `_REFUSAL_PATTERNS[1]` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` so indirect polar `\bwhether\s+...meeting` compliance inquiries refuse inside WH-questions, inquiry-governed `(?:if|that)` clauses refuse with optional indirect objects (`me|us`), and polite-prefaced informational WH-conditionals (`"Could you explain what happens if..."`) are preserved (`RV-048`).

### `P01-T02`: Regression Tests, Documentation, and Verification

* Added `test_c18_renderer_bundle_mutation_isolation_and_whether_vs_prefaced_wh_if_precision` in `src/core/tests/test_regulatory_eval_gates_216.py` and updated `src/core/README.md`.
* Verified in `src/core`:
  * `python3 -m mypy`: `Success: no issues found in 318 source files`
  * `python3 -m ruff check .`: `All checks passed!`
  * `python3 -m ruff format --check .`: `265 files already formatted`
  * `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 21 tests ... OK`
  * `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`: `Ran 58 tests ... OK`

## Blockers and Remaining Work

* Blockers: None.
* Remaining active-plan work: None (`P01`, `P01-T01`, and `P01-T02` completed).
