<!-- markdownlint-disable-file -->
# Research Synthesis: Child Hardening Pass 20 for Issue #216 (`RV-051`..`RV-052`)

* Task ID: `216-citation-eval-2142-c20`
* Parent Task ID: `216-citation-eval-2142-c19`
* Date: `2026-11-14`
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Scope and Evidence

Targeted closure of `RV-051` and `RV-052` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c19-review.md` inside `src/core`:

1. `RV-051` (Coordinated / multi-word obligation modifiers in `_OBLIGATION_OBJECT_RE`):
   * Expand `_OBLIGATION_PREPOSITION_GUARD_RE` to block prepositions (`about|on|for|with|at|in|to|from|by|of|over|into|around|regarding|concerning|before|after|during|until|since|under|within|through|between|across|against|without`) and clause subordinators/finite auxiliaries (`when|where|while|if|unless|whether|that|which|who|what|why|how|is|are|was|were|be|been|has|have|had|do|does|did|will|would|can|could|should|may|might|must`), and widen the `[a-z0-9',-]+` modifier token bound from `{0,2}` to `{0,6}` so coordinated modifiers such as `"legal and statutory obligations"` and `"damp, mould, and building-safety standards"` match without crossing prepositional or clause boundaries.
2. `RV-052` (Coordinated adverbial phrases in `_MEETING_ADVERBS_RE` and coordinated subjects in `_NON_WH_COND_SPAN_RE`):
   * Extend `_MEETING_ADVERBS_RE` to allow optional comma and coordinating `and|or|nor|but` across up to 4 adverbial/negation/degree units (`"adequately and consistently"`, `"not adequately or consistently"`, `"currently, fully, and consistently"`), and widen `_NON_WH_COND_SPAN_RE` to `{1,10}` tokens.
