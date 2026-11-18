<!-- markdownlint-disable-file -->
# Changes Record: Child Hardening Pass 16 for Issue #216 (`RV-041`..`RV-043`)

* Task ID: `216-citation-eval-2142-c16`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c16-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c16-phase-details.md`
* Critique Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c16-plan-critique.md`
* Status: `Completed`

## Summary

Implemented `P01-T01` and `P01-T02` in `src/core` to close `RV-041`..`RV-043` (general-subject progressive `"meeting"` refusal precision + expanded `_COMPLIANCE_SUBJECT_RE`, exact UTC-instant `_aware_dt` observation bounds against `eval_now` and `obs_dt <= rec_dt`, and `_UnsetType`-typed automatic `enforce_ship_gate` activation when `ship_gate_comparison` is supplied plus `RegulatoryChat.ship_gated`).

## Task Progress

* [x] `P01-T01`: Update `regulatory_eval_gates.py` and `regulatory_chat.py` (`RV-041`..`RV-043`).
* [x] `P01-T02`: Add `test_c16_general_subject_meeting_refusal_instant_observation_bounds_and_auto_ship_gate`, update `src/core/README.md`, and pass all `src/core` checks.

## Divergences and Amendments

* Local judgment: used `class _UnsetType(Enum)` sentinel in `regulatory_chat.py` so `mypy` statically enforces `Mapping[str, Any] | None | _UnsetType` on both `ship_gate_comparison` and `surface(..., comparison=...)`.

## Validation Evidence

* `python3 -m mypy`: `Success: no issues found in 318 source files`
* `python3 -m ruff check .` and `python3 -m ruff format --check .`: `All checks passed!`, `265 files already formatted`
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `19` tests `OK`
* `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`: `58` tests `OK`
