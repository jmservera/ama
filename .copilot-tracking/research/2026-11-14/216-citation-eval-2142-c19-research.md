<!-- markdownlint-disable-file -->
# Research Synthesis: Child Hardening Pass 19 for Issue #216 (`RV-049`..`RV-050`)

* Task ID: `216-citation-eval-2142-c19`
* Parent Task ID: `216-citation-eval-2142-c18`
* Date: `2026-11-14`
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Scope and Evidence

Targeted closure of `RV-049` and `RV-050` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c18-review.md` inside `src/core`:

1. `RV-049`:
   * Introduce `_MEETING_ADVERBS_RE = r"(?:(?:not|never|still|already|now|yet|[a-z]+ly)\s+){0,2}"` and `_NON_WH_COND_SPAN_RE = r"(?:(?!(?:what|which|when|where|how|who|why|if|unless|whenever|while)\b)[a-z0-9'_,-]+\s+){1,8}"` in `regulatory_eval_gates.py`.
   * Replace the fixed 5-adverb list before `meeting` with `_MEETING_ADVERBS_RE` (covering `"adequately"`, `"properly"`, `"not adequately"`, etc.), forbid WH/conditional subordinators across every progressive `meeting` pre-verb span, allow optional `that` after `confirm`/`verify`/`certify`/`declare`/`state`/`say`, and replace the wildcard gerund branch (`check...[^.;!?]{0,40}...meeting`) with a direct gerund match (`confirm|verify|certify|declare|state|check` + optional possessive + `_MEETING_ADVERBS_RE` + `meeting`) so `"Please check what happens if the team is meeting statutory obligations."` never false-refuses.
2. `RV-050`:
   * Update `_tampering_render` in `test_regulatory_eval_gates_216.py` so it mutates a supported `snap` in place (`snap["refusal"] = ...`, `snap["sources"] = []`, `snap["facts"] = []`, `snap["cards"] = []`) and returns `render_extractive_answer(snap)` on a supported non-refusal question (`"What do the approved hazard provisions record for this home?"`). Without `copy.deepcopy(snap)`, `render_extractive_answer(snap)` produces a valid refusal envelope matching the mutated `snap`; with `copy.deepcopy(snap)`, `ask()` raises `ChatForbidden` and `surface()` falls back to `cards_only` with non-empty deterministic cards.
