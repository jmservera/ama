<!-- markdownlint-disable-file -->
# Research Synthesis: Child Hardening Pass 16 for Issue #216 (`RV-041`..`RV-043`)

* Task ID: `216-citation-eval-2142-c16`
* Parent Task ID: `216-citation-eval-2142-c15`
* Date: `2026-11-14`
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Scope and Evidence Examined

* `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c15-review.md` (`RV-041`..`RV-043`)
* `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_COMPLIANCE_SUBJECT_RE`, `_REFUSAL_PATTERNS[1]`, `_score_paired_observations`, `compare_chat_against_rule_cards`)
* `src/core/src/zava_forward/core/regulatory_chat.py` (`RegulatoryChat.__init__`, `start`, `ask`, `surface`)
* `src/core/tests/test_regulatory_chat.py` and `src/core/tests/test_regulatory_eval_gates_216.py`

## Findings

1. **`RV-041` (General-subject progressive `"meeting"` refusal precision)**:
   * Expanding `_COMPLIANCE_SUBJECT_RE` with `housing\s+associations?|associations?|organi[sz]ations?|providers?|contractors?|programmes?|services?|teams?|plans?|polic(?:y|ies)|processes?|approaches?|assessments?|inspections?|responses?|actions?|schedules?` covers organizational compliance subjects across all branches of `_REFUSAL_PATTERNS[1]`.
   * In addition, progressive transitive `meeting` + `_OBLIGATION_OBJECT_RE` does not need an enumerated subject allowlist when gated by:
     * clause-initial `(?:^|[.;!?]\s*)\s*(?:is|are|was|were)\b(?!\s+there\b)` without appointment verbs (`hav(?:e|ing)|hold(?:ing)?|schedul(?:e|ed|ing)|book(?:ed|ing)?|arrang(?:e|ed|ing)|attend(?:ing)?`) and without noun determiners (`(?<!\ba\s)(?<!\ban\s)(?<!\bthe\s)(?<!\bany\s)(?<!\bfor\s)(?<!\bof\s)(?<!\bin\s)(?<!\bat\s)(?<!\bby\s)`) immediately before `meeting`,
     * declarative/subordinate `(?:(?:^|[.;!?]\s*)\s*(?!what\b|which\b|when\b|where\b|how\b|who\b)|\b(?:whether|if|that)\s+)[^.;!?]{1,55}\b(?:is|are|was|were)\s+(?:not\s+|currently\s+|fully\s+|still\s+|already\s+)?meeting`,
     * and compliance-assertion verbs (`confirm|verify|certify|declare|state|say|check|decide`) + `meeting`.
2. **`RV-042` (Exact UTC instant comparison on `observed_at` / `recorded_at`)**:
   * Passing `eval_now: datetime | None` (`parsed_now`) into `_score_paired_observations` and parsing `observed_at` / `recorded_at` via `_aware_dt` rejects ambiguous date-only strings (`"2026-10-16"`), rejects same-day post-evaluation timestamps (`obs_dt > eval_now` or `rec_dt > eval_now`), rejects `obs_dt > rec_dt` or UTC-day mismatch when both are supplied, and preserves `obs_day >= thresholds_agreed_day` and `earliest_obs_day`.
3. **`RV-043` (Automatic ship-gate enforcement when `ship_gate_comparison` is supplied + `RegulatoryChat.ship_gated`)**:
   * Because offline evaluation suites (`test_regulatory_chat.py` for `#214` and `_run_suite()` for `#216`) must execute `RegulatoryChat.start()` and `RegulatoryChat.ask()` *before* a paired comparison exists in order to produce the evaluated chat turns, unconfigured `RegulatoryChat(iso, law, render, classify, refuse, ...)` (`ship_gate_comparison is _UNSET` and `enforce_ship_gate is None`) preserves `#214` harness behavior while `surface()` always defaults to `cards_only`.
   * Changing `ship_gate_comparison: Mapping[str, Any] | None | object = _UNSET` and `enforce_ship_gate: bool | None = None` so `self._enforce_ship_gate = (ship_gate_comparison is not _UNSET) if enforce_ship_gate is None else enforce_ship_gate` ensures ANY caller passing `ship_gate_comparison=...` (including `None` or a failing report) automatically enforces `_require_ship_gate()` on `start()` and `ask()` unless `enforce_ship_gate=False` is explicitly requested, and adding `@classmethod def ship_gated(...)` constructs a fail-closed ship-gated `RegulatoryChat` (`enforce_ship_gate=True`) even when `ship_gate_comparison=None`.
