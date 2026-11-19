<!-- markdownlint-disable-file -->
# Research Synthesis: Child Hardening Pass 21 for Issue #216 (`RV-053`..`RV-054`)

* Task ID: `216-citation-eval-2142-c21`
* Parent Task ID: `216-citation-eval-2142-c20`
* Date: `2026-11-14`
* Research Disposition: `executed`
* Planning Readiness: `Ready`

## Scope and Evidence

Targeted closure of `RV-053` and `RV-054` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c20-review.md` inside `src/core`:

1. `RV-053`: Allow `&` and `/` separators inside `_OBLIGATION_OBJECT_RE` modifier tokens (`(?:[a-z0-9',/-]+|&)\s+`) and `_MEETING_ADVERBS_RE` conjunctions (`(?:(?:and(?:/or)?|&|or|nor|but)\s+)?`) so `"health & safety obligations"` and `"legal and/or statutory obligations"` match cleanly.
2. `RV-054`: Guard `_OBLIGATION_PREPOSITION_GUARD_RE` against intransitive temporal/locative post-`meeting` words (`tomorrow|today|tonight|yesterday|soon|later|here|there|online|remotely|together|privately|regularly|weekly|monthly|daily|monday|tuesday|wednesday|thursday|friday|saturday|sunday`) and coordinated discussion/agenda participles (`discussing|reviewing|talking|chatting|speaking|presenting|debating|briefing|updating|considering|examining|exploring|looking|working|voting|deciding|agreeing`) so `"Is the team meeting tomorrow and discussing damp legal obligations?"` does not cross into the second coordinated verb phrase.
