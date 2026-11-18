<!-- markdownlint-disable-file -->
# Review Log: Issue #216 Child Hardening Pass 8 (`216-citation-eval-2142-c8`)

## Metadata

* Task ID: 216-citation-eval-2142-c8
* Parent Task ID: 216-citation-eval-2142-c7
* Date: 2026-11-14
* Review Execution Status: Complete
* Review Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c8-research.md
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md
* Phase Details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md
* Plan Critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c8-plan-critique.md
* Implementation Changes: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c8-changes.md
* Prior Review: .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c7-review.md

## Validation Evidence

* `python3 -m mypy`: `Success: no issues found in 318 source files`
* `python3 -m ruff check .`: `All checks passed!`
* `python3 -m ruff format --check .`: `265 files already formatted`
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 11 tests in 16.242s - OK`
* `PYTHONPATH=src:tests python3 -m unittest test_regulatory_chat test_gates test_live_doc_links -q`: `Ran 58 tests in 34.328s - OK`
* Independent read-only `rubber-duck` subagent review completed against `src/core` changed files and `c8` tracking records; verified zero `.copilot-tracking/` references in `src/core`.

## Plan and Critique Reconciliation

* All `P01`, `P01-T01`, and `P01-T02` markers in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md` are checked and reconciled with `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c8-changes.md`.
* Prior findings `RV-010`, `RV-011`, and `RV-012` are fully resolved; `RV-008`, `RV-009`, `RV-013`, `RV-014`, and critique dispositions `PC-001`..`PC-005` resolved their targeted probes while exposing three remaining fail-closed edge cases recorded below as `RV-015`..`RV-017`.
* Out-of-scope follow-up items (`src/api` route wiring and `src/agents` helper deduplication) remain explicitly separated from the `src/core` boundary.

## Findings

* `RV-015` (High, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c9`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_classify_refusal_confusion`, `evaluate_citation_and_refusal_gates`). A response labelled `kind="refused"` with no citations is classified `invalid_response` even when its `reply` says `"Approved. Close the hazard and clear the safety stop."` or omits `requires_human=True` / matching refusal `reason`. Under owner-agreed `min_rates < 1.0`, `invalid_response` on a mandatory-refusal prompt or answer turn is not blocked by `ref_blockers`/`cit_blockers`, allowing an unsafe malformed refusal or ungrounded answer to pass both gates and enable `chat_with_cards`. Only contract-valid conservative `false_refusal` envelopes may pass sub-`1.0` tolerances; any `unsafe_non_refusal` or `invalid_response` must block gate passage.
* `RV-016` (High, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c9`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`deterministic_rule_cards`, `_baseline_projection_matches`). `deterministic_rule_cards` filters sources and cards with `require_active=False`, so when `resolve_regulatory_surface` falls back to `cards_only` on a direct bundle containing future-dated (`effective="2099-01-01"` > `as_of`), draft/held, unreviewed, partial, or `exercise=False` cards/provisions, `rule_cards["cards"]` and `rule_cards["provisions"]` expose non-active authority as actionable cards. Actionable `cards` and `provisions` on non-conflict surfaces must require active, `as_of`-current provenance, while `conflict` bundles expose conflicting provisions under explicit `conflict=True` (with `cards=[]` unless active) without presenting inactive authority as active rule cards.
* `RV-017` (Medium, Blocking — Destination: `rpi-implement` via child task `216-citation-eval-2142-c9`):
  * Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_id_version_matches`). `ver_token.isdigit()` accepts non-ASCII Unicode superscript/digit characters such as `'²'` (`"card@v²"`) for which `int(ver_token)` raises `ValueError`, and accepts unbounded >4300-digit ASCII digit strings (`f"card@v{'9' * 5000}"`) for which `int(ver_token)` raises `ValueError` (`Exceeds the limit (4300 digits)`). Restrict `ver_token` to bounded ASCII digits (`ver_token.isascii() and ver_token.isdigit() and len(ver_token) <= 18`) before `int(...)` conversion.
* Follow-up (Out of Scope — Destination: distinct cross-package follow-up outside `src/core`):
  * Wiring `RegulatoryChat.surface` / `resolve_regulatory_surface` into `src/api/src/zava_forward/api/server.py` and deduplicating `src/agents` helpers remain outside the user-bounded `src/core` deliverable.
