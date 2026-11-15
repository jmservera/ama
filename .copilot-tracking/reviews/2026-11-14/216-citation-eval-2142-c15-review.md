<!-- markdownlint-disable-file -->
# Review Record: Child Hardening Pass 15 for Issue #216 (`216-citation-eval-2142-c15`)

* Task ID: `216-citation-eval-2142-c15`
* Parent Task ID: `216-citation-eval-2142-c14`
* Date: `2026-11-14`
* Execution Status: `Complete`
* Outcome: `Defects found`

## Compared Artifacts

* Research: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c15-research.md`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c15-plan.md`
* Phase Details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c15-phase-details.md`
* Plan Critique: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c15-plan-critique.md`
* Changes Record: `.copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c15-changes.md`
* Prior Review: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c14-review.md`

## Boundary Reconciliation and Closure Verification

* Plan markers (`P01`, `P01-T01`, `P01-T02`), phase details, changes record, and validation results (`mypy` 0 issues across 318 files, `ruff check .`, `ruff format --check .`, 18 Issue #216 tests, 58 companion `src/core` tests) are reconciled.
* Prior findings `RV-039` (day-level mandatory observation timestamps) and `RV-040` (pre-observation `agreed_on` bound) are implemented, and noun-`"meeting"` prompts no longer false-refuse; an independent read-only `rubber-duck` lens bounded to `src/core` identified three remaining high-confidence gaps (`RV-041`..`RV-043`) routed to child task `216-citation-eval-2142-c16`.
* Pre-existing `.copilot-tracking` string literals in `src/core/src/zava_forward/core/synthetic/cutover_audit.py`, `src/core/tests/test_cutover_audit.py`, and `src/core/tests/test_live_doc_links.py` belong to repository-wide directory-skip rules on `main`; none of the Issue #216 files (`regulatory_eval_gates.py`, `regulatory_chat.py`, `test_regulatory_eval_gates_216.py`, `src/core/README.md`) contain `.copilot-tracking` references.

## Findings

### `RV-041` (High): Progressive compliance `"meeting"` restricted to `_COMPLIANCE_SUBJECT_RE` misses organizational subjects such as `"housing association"`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_COMPLIANCE_SUBJECT_RE` and `_REFUSAL_PATTERNS[1]`). `"Is our housing association meeting statutory requirements for this damp home?"` is not matched because `"housing association"` is not in `_COMPLIANCE_SUBJECT_RE`, yet `"damp home"` triggers a supported hazard retrieval purpose instead of refusing.
* Impact: Staff asking whether the housing association, organisation, provider, contractor, or team is meeting statutory requirements can bypass compliance refusal.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c16`: broaden `_COMPLIANCE_SUBJECT_RE` to include organizational/service subjects and match yes/no or declarative progressive `meeting` + `_OBLIGATION_OBJECT_RE` across general subjects while keeping noun-`"meeting"`, article/preposition, and `what/which/when/where/how` exclusions).

### `RV-042` (High): Same-day future timestamps and bare date-only strings on `observed_at` / `recorded_at` pass day-granularity comparison against `now`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_score_paired_observations`). Reducing `observed_at` / `recorded_at` via `_extract_day` allows `"2026-10-16T23:59:00+00:00"` (or an ambiguous bare date `"2026-10-16"`) to establish measured value at `now = 2026-10-16T12:00:00+00:00`.
* Impact: Post-evaluation same-day timestamps or ambiguous date-only strings are accepted instead of failing closed against the exact UTC evaluation instant.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c16`: require timezone-aware UTC timestamps via `_aware_dt` on `observed_at` / `recorded_at`, enforce `obs_dt <= eval_now` and `rec_dt <= eval_now`, enforce `obs_dt <= rec_dt` when both are supplied, and preserve UTC-date `>= thresholds_agreed_day` and `earliest_obs_day` checks).

### `RV-043` (Medium): `RegulatoryChat` ignores supplied `ship_gate_comparison` on `start()` / `ask()` unless `enforce_ship_gate=True` is also set

* Evidence: `src/core/src/zava_forward/core/regulatory_chat.py` (`RegulatoryChat.__init__`). Passing `ship_gate_comparison=failed_cmp` (or `ship_gate_comparison=None`) leaves `enforce_ship_gate=False` unless the caller separately sets `enforce_ship_gate=True`, and there is no fail-closed `RegulatoryChat.ship_gated(...)` constructor for production ship-gated wiring.
* Impact: A caller supplying `ship_gate_comparison` without `enforce_ship_gate=True` leaves `start()` and `ask()` open despite an explicit `ship_cards_only` comparison result.
* Recommended destination: `rpi-implement` (via child task `216-citation-eval-2142-c16`: use `_UNSET` sentinel for `ship_gate_comparison` and `enforce_ship_gate: bool | None = None` so supplying `ship_gate_comparison` — including `None` — automatically enables `enforce_ship_gate=True` on `start()` and `ask()`, add `RegulatoryChat.ship_gated(...)` classmethod with `enforce_ship_gate=True` by default, and preserve unconfigured `#214` offline evaluation harness construction where `ship_gate_comparison is _UNSET` and `enforce_ship_gate is None`).

## Validation Coverage

* `python3 -m mypy` in `src/core`: `0` issues in `318` source files.
* `python3 -m ruff check .` and `python3 -m ruff format --check .` in `src/core`: passed.
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `18` passed.
* `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`: `58` passed.

## Routed Follow-Up

1. Child task `216-citation-eval-2142-c16`: close `RV-041`..`RV-043` in `src/core` (`regulatory_eval_gates.py`, `regulatory_chat.py`, `test_regulatory_eval_gates_216.py`, `src/core/README.md`).
2. Cross-package runtime wiring (`src/api` and `src/agents`, outside `src/core` scope).
